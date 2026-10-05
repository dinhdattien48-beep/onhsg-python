import os
import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
import bcrypt
import jwt

from database import get_connection

# === Cấu hình Auth & JWT ===
SECRET_KEY = os.environ.get("JWT_SECRET", "default_secret_key_if_not_set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

# === Cấu hình Mail ===
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "")
SMTP_APP_PASSWORD = os.environ.get("SMTP_APP_PASSWORD", "")

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])
admin_router = APIRouter(prefix="/api/admin", tags=["admin"])


# === Models ===
class SendOTPRequest(BaseModel):
    email: EmailStr

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    otp_code: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RoleUpdateRequest(BaseModel):
    role: str


# === Helper Functions ===
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def send_email_otp(to_email: str, otp: str):
    if not SMTP_EMAIL or not SMTP_APP_PASSWORD:
        raise Exception("Chưa cấu hình SMTP_EMAIL hoặc SMTP_APP_PASSWORD trong .env")
    
    msg = MIMEText(f"Mã xác thực OTP đăng ký tài khoản HSG Python của bạn là: {otp}\n\nMã này sẽ hết hạn sau 5 phút.")
    msg['Subject'] = 'Mã xác thực đăng ký HSG Python'
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
    server.send_message(msg)
    server.quit()


# === Middleware / Dependency lấy User hiện tại ===
from fastapi.security import OAuth2PasswordBearer
# Tạm dùng header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login_swagger", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chưa đăng nhập")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token đã hết hạn hoặc không hợp lệ")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, email, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại")
    return dict(user)

def require_owner(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "Owner":
        raise HTTPException(status_code=403, detail="Không có quyền truy cập (Yêu cầu quyền Owner)")
    return current_user


# === API Auth ===
@auth_router.post("/send-otp")
async def api_send_otp(req: SendOTPRequest):
    conn = get_connection()
    cursor = conn.cursor()
    # Kiểm tra email đã tồn tại chưa
    cursor.execute("SELECT id FROM users WHERE email = ?", (req.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email này đã được đăng ký.")
    
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.now() + timedelta(minutes=5)
    
    # Ghi vào DB
    cursor.execute("""
        INSERT INTO otp_codes (email, otp_code, expires_at) VALUES (?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET otp_code = ?, expires_at = ?
    """, (req.email, otp, expires_at, otp, expires_at))
    conn.commit()
    conn.close()
    
    # Gửi mail
    try:
        send_email_otp(req.email, otp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi gửi mail: {str(e)}")
        
    return {"message": "Mã xác thực đã được gửi tới email của bạn."}


@auth_router.post("/register")
async def api_register(req: RegisterRequest):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Xác thực OTP
    cursor.execute("SELECT otp_code, expires_at FROM otp_codes WHERE email = ?", (req.email,))
    otp_record = cursor.fetchone()
    if not otp_record:
        conn.close()
        raise HTTPException(status_code=400, detail="Chưa yêu cầu mã xác thực cho email này.")
    
    if otp_record["otp_code"] != req.otp_code:
        conn.close()
        raise HTTPException(status_code=400, detail="Mã xác thực không chính xác.")
        
    expires_at = datetime.fromisoformat(otp_record["expires_at"])
    if datetime.now() > expires_at:
        conn.close()
        raise HTTPException(status_code=400, detail="Mã xác thực đã hết hạn.")
        
    # Xóa OTP sau khi dùng
    cursor.execute("DELETE FROM otp_codes WHERE email = ?", (req.email,))
    
    # Tạo user
    hashed_pwd = get_password_hash(req.password)
    try:
        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, role)
            VALUES (?, ?, ?, 'Học Sinh')
        """, (req.full_name, req.email, hashed_pwd))
        conn.commit()
    except Exception:
        conn.close()
        raise HTTPException(status_code=400, detail="Lỗi khi tạo tài khoản.")
    
    conn.close()
    return {"message": "Đăng ký tài khoản thành công."}


@auth_router.post("/login")
async def api_login(req: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, email, password_hash, role FROM users WHERE email = ?", (req.email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng.")
        
    access_token = create_access_token(data={"sub": user["email"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"]
        }
    }


@auth_router.get("/profile")
async def api_profile(current_user: dict = Depends(get_current_user)):
    return current_user


# === API Admin (Chỉ Owner) ===
@admin_router.get("/users")
async def api_get_users(current_user: dict = Depends(require_owner)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, email, role, created_at FROM users ORDER BY created_at DESC")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"users": users}


@admin_router.put("/users/{user_id}/role")
async def api_update_user_role(user_id: int, req: RoleUpdateRequest, current_user: dict = Depends(require_owner)):
    valid_roles = ["Học Sinh", "Giáo Viên", "Owner"]
    if req.role not in valid_roles:
        raise HTTPException(status_code=400, detail="Vai trò không hợp lệ.")
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (req.role, user_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    conn.commit()
    conn.close()
    
    return {"message": f"Đã cập nhật vai trò thành {req.role}"}

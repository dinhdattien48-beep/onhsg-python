import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load .env explicitly
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "")
SMTP_APP_PASSWORD = os.environ.get("SMTP_APP_PASSWORD", "")

print(f"SMTP_EMAIL: {SMTP_EMAIL}")
print(f"SMTP_APP_PASSWORD_LENGTH: {len(SMTP_APP_PASSWORD) if SMTP_APP_PASSWORD else 0}")

if not SMTP_EMAIL or not SMTP_APP_PASSWORD:
    print("Missing SMTP config in .env")
    exit(1)

try:
    print("Connecting to SMTP_SSL...")
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
    server.set_debuglevel(1)  # Bật debug để in chi tiết lỗi
    print("Logging in...")
    server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
    print("Logged in successfully.")
    
    msg = MIMEText("Test email")
    msg['Subject'] = 'Test'
    msg['From'] = SMTP_EMAIL
    msg['To'] = SMTP_EMAIL
    
    print("Sending message...")
    server.send_message(msg)
    server.quit()
    print("Message sent successfully.")
except Exception as e:
    print(f"Error: {e}")

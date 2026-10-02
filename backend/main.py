"""
main.py - FastAPI Backend chính cho nền tảng luyện thi HSG Tin học Python.
Cung cấp API cho: lộ trình, bài giảng, chấm bài, AI Mentor, tiến độ.
"""

import os
import sys
import json

# Đảm bảo thư mục backend nằm trong sys.path để import an toàn dù chạy từ thư mục gốc hay backend
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Tự động nạp biến môi trường từ file .env nếu có (tiện lợi khi chạy local)
for _env_candidate in [os.path.join(os.path.dirname(BACKEND_DIR), ".env"), os.path.join(BACKEND_DIR, ".env")]:
    if os.path.exists(_env_candidate):
        try:
            with open(_env_candidate, "r", encoding="utf-8") as _f:
                for _line in _f:
                    _line = _line.strip()
                    if _line and not _line.startswith("#") and "=" in _line:
                        _k, _v = _line.split("=", 1)
                        _k = _k.strip()
                        _v = _v.strip().strip("'\"")
                        if _k and _k not in os.environ:
                            os.environ[_k] = _v
        except Exception:
            pass

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from seed_data import get_all_stages, get_stage, get_problem, get_test_cases
from judge import judge_submission
from ai_mentor import analyze_student_code
from database import (
    save_submission, get_progress, get_submissions,
    save_setting, get_setting
)

# ============================================================================
# KHỞI TẠO APP
# ============================================================================

app = FastAPI(
    title="HSG Python - Luyện thi Học Sinh Giỏi Tin học",
    description="Nền tảng dạy và luyện thi HSG Tin học bằng Python từ con số 0",
    version="1.0.0"
)

# CORS cho phép frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# ============================================================================
# MODELS
# ============================================================================

class SubmitRequest(BaseModel):
    problem_id: str
    code: str
    api_key: Optional[str] = None
    model_name: Optional[str] = None


class RunRequest(BaseModel):
    code: str
    input_data: str = ""


class SettingsRequest(BaseModel):
    api_key: str = ""
    model_name: str = "gemini-3.8-flash"


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Endpoint nhẹ kiểm tra server còn hoạt động (chống sleep 24/24)."""
    return {"status": "alive"}


async def keep_alive_background_task():
    """Background task: mỗi 10 phút tự động gửi GET /health tới RENDER_EXTERNAL_URL để giữ server Render luôn thức 24/24."""
    import asyncio
    import httpx

    # Chờ 60 giây sau khi server khởi động
    await asyncio.sleep(60)
    while True:
        render_url = os.environ.get("RENDER_EXTERNAL_URL", "").strip() or os.environ.get("PING_URL", "").strip()
        if render_url:
            health_url = render_url.rstrip("/") + "/health"
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    res = await client.get(health_url)
                    print(f"[Keep-Alive 24/7] Ping thành công {health_url} - Status {res.status_code}")
            except Exception as e:
                print(f"[Keep-Alive 24/7] Ping {health_url} gặp lỗi: {e}")
        # Chờ 10 phút (600 giây)
        await asyncio.sleep(600)


@app.on_event("startup")
async def startup_event():
    import asyncio
    asyncio.create_task(keep_alive_background_task())


@app.get("/")
async def serve_frontend():
    """Serve trang chủ frontend."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "HSG Python API - Frontend chưa được cài đặt"}


@app.get("/api/stages")
async def list_stages():
    """Lấy danh sách tất cả các chặng học tập."""
    stages = get_all_stages()
    # Trả về danh sách rút gọn (không kèm theory dài)
    result = []
    for s in stages:
        result.append({
            "id": s["id"],
            "title": s["title"],
            "icon": s["icon"],
            "problems": [
                {
                    "id": p["id"],
                    "title": p["title"],
                    "difficulty": p["difficulty"],
                    "order": p["order"],
                }
                for p in s["problems"]
            ]
        })
    return {"stages": result}


@app.get("/api/stages/{stage_id}")
async def get_stage_detail(stage_id: int):
    """Lấy chi tiết một chặng (lý thuyết + vũ khí + danh sách bài tập)."""
    stage = get_stage(stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Không tìm thấy chặng này")
    return {
        "id": stage["id"],
        "title": stage["title"],
        "icon": stage["icon"],
        "theory": stage["theory"],
        "weapon": stage["weapon"],
        "problems": [
            {
                "id": p["id"],
                "title": p["title"],
                "difficulty": p["difficulty"],
                "order": p["order"],
                "description": p["description"],
                "time_limit": p["time_limit"],
            }
            for p in stage["problems"]
        ]
    }


@app.get("/api/problems/{problem_id}")
async def get_problem_detail(problem_id: str):
    """Lấy chi tiết một bài tập."""
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài tập")
    return {
        "id": problem["id"],
        "stage_id": problem["stage_id"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "description": problem["description"],
        "time_limit": problem["time_limit"],
    }


@app.post("/api/run")
async def run_code(req: RunRequest):
    """Chạy thử code với input tùy chọn (không chấm điểm)."""
    import subprocess
    import sys
    import tempfile
    import time

    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code không được rỗng")

    tmp_file = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8'
        )
        tmp_file.write(req.code)
        tmp_file.close()

        start = time.perf_counter()
        process = subprocess.run(
            [sys.executable, "-u", tmp_file.name],
            input=req.input_data,
            capture_output=True,
            text=True,
            timeout=5.0,
            cwd=tempfile.gettempdir(),
        )
        elapsed = time.perf_counter() - start

        return {
            "output": process.stdout,
            "error": process.stderr,
            "time_ms": round(elapsed * 1000, 1),
            "return_code": process.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": "Chương trình chạy quá 5 giây!",
            "time_ms": 5000,
            "return_code": -1,
        }
    except Exception as e:
        return {
            "output": "",
            "error": str(e),
            "time_ms": 0,
            "return_code": -1,
        }
    finally:
        if tmp_file and os.path.exists(tmp_file.name):
            try:
                os.unlink(tmp_file.name)
            except OSError:
                pass


@app.post("/api/submit")
async def submit_code(req: SubmitRequest):
    """Nộp bài chấm 10 test cases + AI Mentor nhận xét."""
    problem = get_problem(req.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài tập")

    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code không được rỗng")

    # 1. Sinh 10 test cases
    test_cases = get_test_cases(req.problem_id)
    if not test_cases:
        raise HTTPException(status_code=500, detail="Không sinh được test cases")

    # 2. Chấm bài
    judge_result = judge_submission(
        student_code=req.code,
        test_cases=test_cases,
        time_limit=problem.get("time_limit", 1.0)
    )

    # 3. Gọi AI Mentor: nếu người dùng không truyền api_key thì tự động lấy từ biến môi trường
    ai_feedback = ""
    api_key = (req.api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip() or get_setting("api_key", "").strip()
    model_name = (req.model_name or "").strip() or os.environ.get("GEMINI_MODEL", "").strip() or get_setting("model_name", "").strip() or "gemini-3.8-flash"

    if api_key:
        try:
            ai_feedback = analyze_student_code(
                api_key=api_key,
                model_name=model_name,
                problem_desc=problem["description"],
                student_code=req.code,
                judge_results={
                    "score": judge_result["score"],
                    "total": judge_result["total"],
                    "details": [
                        {
                            "test": r["test"],
                            "status": r["status"],
                            "time_ms": r["time_ms"]
                        }
                        for r in judge_result["results"]
                    ]
                }
            )
        except Exception as e:
            ai_feedback = f"⚠️ Lỗi khi gọi AI Mentor: {str(e)}"
    else:
        ai_feedback = "💡 Hãy cấu hình biến môi trường `GEMINI_API_KEY` trên server để nhận nhận xét và hướng dẫn tối ưu code tự động từ AI Mentor!"

    # 4. Lưu kết quả
    save_submission(
        problem_id=req.problem_id,
        stage_id=problem["stage_id"],
        code=req.code,
        score=judge_result["score"],
        total_tests=judge_result["total"],
        status="AC" if judge_result["score"] == judge_result["total"] else "WA",
        results=judge_result["results"],
        ai_feedback=ai_feedback,
    )

    # 5. Trả về kết quả đầy đủ cho tất cả 10 test (không ẩn test 6-10)
    sanitized_results = []
    for r in judge_result["results"]:
        entry = {
            "test": r["test"],
            "status": r["status"],
            "time_ms": r["time_ms"],
            "input": r["input"][:2000] if len(r.get("input", "")) > 2000 else r.get("input", ""),
            "student_output": r.get("student_output", "")[:2000],
            "expected_output": r.get("expected_output", "")[:2000],
            "error": r.get("error", "")[:500] if r.get("error") else "",
        }
        sanitized_results.append(entry)

    return {
        "score": judge_result["score"],
        "total": judge_result["total"],
        "results": sanitized_results,
        "ai_feedback": ai_feedback,
    }


@app.get("/api/progress")
async def get_student_progress():
    """Lấy tiến độ học tập tổng hợp."""
    progress = get_progress()
    return {"progress": progress}


@app.get("/api/submissions/{problem_id}")
async def get_problem_submissions(problem_id: str, limit: int = 5):
    """Lấy lịch sử nộp bài."""
    subs = get_submissions(problem_id, limit)
    return {"submissions": subs}


@app.post("/api/settings")
async def update_settings(req: SettingsRequest):
    """Cập nhật cài đặt API key và model name."""
    if req.api_key:
        save_setting("api_key", req.api_key)
    if req.model_name:
        save_setting("model_name", req.model_name)
    return {"status": "ok", "message": "Đã lưu cài đặt"}


@app.get("/api/settings")
async def get_settings():
    """Lấy cài đặt hiện tại (bảo mật: không gửi API Key của giáo viên về trình duyệt)."""
    has_server_key = bool(os.environ.get("GEMINI_API_KEY", "").strip() or get_setting("api_key", "").strip())
    default_model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash").strip()
    return {
        "api_key": "",  # Bảo mật: không để lộ API key giáo viên cho học sinh
        "model_name": os.environ.get("GEMINI_MODEL", "").strip() or get_setting("model_name", default_model),
        "has_server_key": has_server_key,
    }


# ============================================================================
# CHẠY SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    import sys
    import io
    # Fix Unicode output on Windows console
    if sys.platform == "win32":
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass

    # Đọc cổng từ biến môi trường PORT (tương thích Render, Hugging Face Spaces hoặc mặc định 8000/7860)
    port = int(os.environ.get("PORT", 8000))
    print("=" * 60)
    print("HSG Python - Luyen thi Hoc Sinh Gioi Tin hoc")
    print("=" * 60)
    print(f"Truy cap: http://0.0.0.0:{port}")
    print(f"API Docs: http://0.0.0.0:{port}/docs")
    print("=" * 60)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

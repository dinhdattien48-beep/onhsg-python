"""
classroom.py - Module quản lý Lớp Học & Bài Tập Giáo Viên Giao.
Cung cấp API cho Giáo Viên (quản lý học sinh, giao bài, theo dõi tiến độ, xem lịch sử nộp bài)
và Học Sinh (nhập mã lớp, nhận bài tập được giao, nộp bài, nhận phản hồi AI).
"""

import os
import json
import random
import string
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from database import get_connection, get_setting
from auth import get_current_user
from judge import judge_submission
from ai_mentor import analyze_student_code

classroom_router = APIRouter(prefix="/api/classroom", tags=["classroom"])


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class CreateClassRequest(BaseModel):
    class_name: str
    class_code: Optional[str] = None


class JoinClassRequest(BaseModel):
    class_code: str


class TestCaseModel(BaseModel):
    input: str
    expected_output: str


class CreateAssignmentRequest(BaseModel):
    title: str
    description: str
    time_limit: Optional[float] = 1.0
    test_cases: List[TestCaseModel]
    deadline: Optional[str] = None


class SubmitAssignmentRequest(BaseModel):
    code: str
    api_key: Optional[str] = None
    model_name: Optional[str] = None


# ============================================================================
# HELPERS
# ============================================================================

def generate_random_class_code(length: int = 6) -> str:
    """Tạo mã lớp ngẫu nhiên dễ nhớ, ví dụ: HSG839, TIN12A"""
    prefix = random.choice(["HSG", "TIN", "PY"])
    chars = "".join(random.choices(string.digits, k=3))
    return f"{prefix}{chars}"


def require_teacher_or_owner(current_user: dict = Depends(get_current_user)):
    """Xác thực người dùng là Giáo Viên hoặc Owner."""
    role = current_user.get("role")
    if role not in ["Giáo Viên", "Owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ tài khoản Giáo Viên hoặc Quản trị viên mới có quyền sử dụng tính năng này."
        )
    return current_user


# ============================================================================
# TEACHER ENDPOINTS
# ============================================================================

@classroom_router.get("/teacher/class")
async def get_teacher_class(teacher: dict = Depends(require_teacher_or_owner)):
    """Lấy thông tin lớp học của giáo viên (Mỗi GV tối đa 1 lớp)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, 
            (SELECT COUNT(*) FROM class_members WHERE class_id = c.id) as student_count,
            (SELECT COUNT(*) FROM class_assignments WHERE class_id = c.id) as assignment_count
        FROM classes c
        WHERE c.teacher_id = ?
    """, (teacher["id"],))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"has_class": False}

    return {
        "has_class": True,
        "class": dict(row)
    }


@classroom_router.post("/teacher/class")
async def create_teacher_class(req: CreateClassRequest, teacher: dict = Depends(require_teacher_or_owner)):
    """Tạo lớp học mới (Ràng buộc: Mỗi giáo viên chỉ được tạo tối đa 1 mã lớp)."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Kiểm tra giáo viên đã có lớp chưa
    cursor.execute("SELECT id, class_code, class_name FROM classes WHERE teacher_id = ?", (teacher["id"],))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"Mỗi tài khoản giáo viên chỉ được tạo tối đa 1 lớp học. Bạn hiện đã có lớp '{existing['class_name']}' với mã lớp là: {existing['class_code']}"
        )

    # 2. Xử lý mã lớp
    code = (req.class_code or "").strip().upper().replace(" ", "")
    if not code:
        code = generate_random_class_code()

    # Kiểm tra trùng mã lớp
    cursor.execute("SELECT id FROM classes WHERE class_code = ?", (code,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail=f"Mã lớp '{code}' đã tồn tại, vui lòng chọn mã khác.")

    class_name = req.class_name.strip()
    if not class_name:
        conn.close()
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên lớp học.")

    cursor.execute("""
        INSERT INTO classes (teacher_id, class_code, class_name)
        VALUES (?, ?, ?)
    """, (teacher["id"], code, class_name))
    class_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "message": "Tạo lớp học thành công!",
        "class": {
            "id": class_id,
            "class_code": code,
            "class_name": class_name,
            "teacher_id": teacher["id"]
        }
    }


@classroom_router.get("/teacher/students")
async def get_teacher_students(teacher: dict = Depends(require_teacher_or_owner)):
    """Lấy danh sách tất cả học sinh trong lớp của giáo viên kèm chỉ số tiến độ."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM classes WHERE teacher_id = ?", (teacher["id"],))
    cls = cursor.fetchone()
    if not cls:
        conn.close()
        return {"students": []}

    class_id = cls["id"]
    cursor.execute("""
        SELECT u.id, u.full_name, u.email, cm.joined_at,
            (SELECT COUNT(*) FROM user_progress up WHERE up.user_id = u.id AND up.completed = 1) as ac_count,
            (SELECT COUNT(*) FROM submissions s WHERE s.user_id = u.id) as submissions_count,
            (SELECT COUNT(DISTINCT assignment_id) FROM assignment_submissions WHERE student_id = u.id) as assignment_done_count,
            (SELECT MAX(submitted_at) FROM submissions s WHERE s.user_id = u.id) as last_active
        FROM class_members cm
        JOIN users u ON cm.student_id = u.id
        WHERE cm.class_id = ?
        ORDER BY cm.joined_at DESC
    """, (class_id,))

    rows = cursor.fetchall()
    conn.close()
    return {"students": [dict(r) for r in rows]}


@classroom_router.get("/teacher/student/{student_id}")
async def get_student_detail(student_id: int, teacher: dict = Depends(require_teacher_or_owner)):
    """Xem chi tiết lộ trình học tập và lịch sử nộp bài (kèm code & nhận xét AI) của học sinh."""
    conn = get_connection()
    cursor = conn.cursor()

    # Xác thực học sinh này có thuộc lớp của giáo viên không
    cursor.execute("""
        SELECT u.id, u.full_name, u.email, cm.joined_at, c.class_name
        FROM class_members cm
        JOIN classes c ON cm.class_id = c.id
        JOIN users u ON cm.student_id = u.id
        WHERE c.teacher_id = ? AND cm.student_id = ?
    """, (teacher["id"], student_id))
    student_info = cursor.fetchone()

    if not student_info and teacher.get("role") != "Owner":
        conn.close()
        raise HTTPException(status_code=404, detail="Không tìm thấy học sinh này trong lớp của bạn.")

    # 1. Lấy tiến độ các bài tập HSG (user_progress)
    cursor.execute("""
        SELECT problem_id, stage_id, completed, best_score, attempts, completed_at
        FROM user_progress
        WHERE user_id = ?
        ORDER BY stage_id ASC
    """, (student_id,))
    progress_rows = cursor.fetchall()

    # 2. Lấy 30 bài nộp gần nhất (Submissions history)
    cursor.execute("""
        SELECT id, problem_id, stage_id, code, score, total_tests, status, results_json, ai_feedback, submitted_at
        FROM submissions
        WHERE user_id = ?
        ORDER BY submitted_at DESC
        LIMIT 30
    """, (student_id,))
    submission_rows = cursor.fetchall()

    # 3. Lấy các bài tập giáo viên giao mà học sinh đã nộp
    cursor.execute("""
        SELECT sub.id, sub.assignment_id, ca.title as assignment_title, sub.code, sub.score, 
               sub.total_tests, sub.status, sub.ai_feedback, sub.submitted_at
        FROM assignment_submissions sub
        JOIN class_assignments ca ON sub.assignment_id = ca.id
        WHERE sub.student_id = ?
        ORDER BY sub.submitted_at DESC
    """, (student_id,))
    assign_sub_rows = cursor.fetchall()

    conn.close()

    # 4. Tổng hợp lộ trình 8 chặng
    from seed_data import get_all_stages
    all_stages = get_all_stages()
    progress_map = {r["problem_id"]: dict(r) for r in progress_rows}

    stages_summary = []
    completed_problems_count = 0
    total_problems_count = 0
    completed_stages_count = 0

    for s in all_stages:
        stg_problems = []
        stg_completed = 0
        for p in s["problems"]:
            p_id = p["id"]
            total_problems_count += 1
            prog = progress_map.get(p_id, {})
            is_comp = prog.get("completed", 0) == 1
            if is_comp:
                stg_completed += 1
                completed_problems_count += 1
            stg_problems.append({
                "id": p_id,
                "title": p["title"],
                "completed": is_comp,
                "best_score": prog.get("best_score", 0),
                "attempts": prog.get("attempts", 0)
            })
        
        if stg_completed == len(s["problems"]) and len(s["problems"]) > 0:
            completed_stages_count += 1

        stages_summary.append({
            "id": s["id"],
            "title": s["title"],
            "icon": s["icon"],
            "completed": stg_completed,
            "total": len(s["problems"]),
            "problems": stg_problems
        })

    roadmap_data = {
        "completed_stages": completed_stages_count,
        "total_stages": len(all_stages),
        "completed_problems": completed_problems_count,
        "total_problems": total_problems_count,
        "stages": stages_summary
    }

    return {
        "student": dict(student_info) if student_info else {"id": student_id, "full_name": "Học sinh"},
        "roadmap": roadmap_data,
        "progress": [dict(r) for r in progress_rows],
        "submissions": [dict(r) for r in submission_rows],
        "assignment_submissions": [dict(r) for r in assign_sub_rows]
    }


@classroom_router.post("/teacher/assignments")
async def create_assignment(req: CreateAssignmentRequest, teacher: dict = Depends(require_teacher_or_owner)):
    """Giáo viên giao bài tập mới cho lớp."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM classes WHERE teacher_id = ?", (teacher["id"],))
    cls = cursor.fetchone()
    if not cls:
        conn.close()
        raise HTTPException(status_code=400, detail="Bạn chưa tạo lớp học. Hãy tạo lớp trước khi giao bài.")

    class_id = cls["id"]
    if not req.title.strip():
        conn.close()
        raise HTTPException(status_code=400, detail="Tiêu đề bài tập không được để trống.")

    if not req.test_cases:
        conn.close()
        raise HTTPException(status_code=400, detail="Cần ít nhất 1 test case mẫu để chấm điểm bài tập.")

    test_cases_json = json.dumps([tc.dict() for tc in req.test_cases], ensure_ascii=False)

    cursor.execute("""
        INSERT INTO class_assignments (class_id, teacher_id, title, description, time_limit, test_cases_json, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (class_id, teacher["id"], req.title.strip(), req.description.strip(),
          req.time_limit or 1.0, test_cases_json, req.deadline))

    assignment_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "message": "Giao bài tập thành công!",
        "assignment_id": assignment_id
    }


@classroom_router.get("/teacher/assignments")
async def get_teacher_assignments(teacher: dict = Depends(require_teacher_or_owner)):
    """Lấy danh sách các bài tập giáo viên đã giao cho lớp."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM classes WHERE teacher_id = ?", (teacher["id"],))
    cls = cursor.fetchone()
    if not cls:
        conn.close()
        return {"assignments": []}

    class_id = cls["id"]
    cursor.execute("""
        SELECT ca.*,
            (SELECT COUNT(DISTINCT student_id) FROM assignment_submissions WHERE assignment_id = ca.id) as submitted_count,
            (SELECT COUNT(DISTINCT student_id) FROM assignment_submissions WHERE assignment_id = ca.id AND score = total_tests) as ac_count
        FROM class_assignments ca
        WHERE ca.class_id = ?
        ORDER BY ca.created_at DESC
    """, (class_id,))

    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        try:
            d["test_cases_count"] = len(json.loads(d["test_cases_json"]))
        except Exception:
            d["test_cases_count"] = 0
        result.append(d)

    return {"assignments": result}


@classroom_router.get("/teacher/assignment/{assignment_id}/submissions")
async def get_assignment_submissions(assignment_id: int, teacher: dict = Depends(require_teacher_or_owner)):
    """Xem danh sách các bài nộp của cả lớp cho một bài tập cụ thể."""
    conn = get_connection()
    cursor = conn.cursor()

    # Kiểm tra assignment có thuộc lớp của giáo viên này không
    cursor.execute("""
        SELECT ca.id, ca.title, ca.class_id
        FROM class_assignments ca
        JOIN classes c ON ca.class_id = c.id
        WHERE ca.id = ? AND c.teacher_id = ?
    """, (assignment_id, teacher["id"]))
    assign = cursor.fetchone()
    if not assign and teacher.get("role") != "Owner":
        conn.close()
        raise HTTPException(status_code=404, detail="Bài tập không tồn tại hoặc không thuộc quyền quản lý của bạn.")

    cursor.execute("""
        SELECT sub.id, sub.student_id, sub.student_name, u.email as student_email,
               sub.code, sub.score, sub.total_tests, sub.status, sub.ai_feedback, sub.submitted_at
        FROM assignment_submissions sub
        JOIN users u ON sub.student_id = u.id
        WHERE sub.assignment_id = ?
        ORDER BY sub.submitted_at DESC
    """, (assignment_id,))

    rows = cursor.fetchall()
    conn.close()
    return {
        "assignment_title": assign["title"] if assign else "Bài tập",
        "submissions": [dict(r) for r in rows]
    }


@classroom_router.delete("/teacher/assignment/{assignment_id}")
async def delete_assignment(assignment_id: int, teacher: dict = Depends(require_teacher_or_owner)):
    """Xóa một bài tập đã giao."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM class_assignments
        WHERE id = ? AND class_id IN (SELECT id FROM classes WHERE teacher_id = ?)
    """, (assignment_id, teacher["id"]))

    if cursor.rowcount == 0 and teacher.get("role") != "Owner":
        conn.close()
        raise HTTPException(status_code=404, detail="Không tìm thấy bài tập để xóa.")

    # Xóa luôn các submission của bài này
    cursor.execute("DELETE FROM assignment_submissions WHERE assignment_id = ?", (assignment_id,))
    conn.commit()
    conn.close()

    return {"message": "Đã xóa bài tập thành công."}


@classroom_router.get("/teacher/live-feed")
async def get_class_live_feed(teacher: dict = Depends(require_teacher_or_owner)):
    """Xem bảng tin nộp bài thời gian thực của cả lớp."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM classes WHERE teacher_id = ?", (teacher["id"],))
    cls = cursor.fetchone()
    if not cls:
        conn.close()
        return {"feed": []}

    cursor.execute("""
        SELECT s.id, s.user_name, s.problem_id, s.score, s.total_tests, s.status, s.submitted_at
        FROM submissions s
        JOIN class_members cm ON s.user_id = cm.student_id
        WHERE cm.class_id = ?
        ORDER BY s.submitted_at DESC
        LIMIT 30
    """, (cls["id"],))

    rows = cursor.fetchall()
    conn.close()
    return {"feed": [dict(r) for r in rows]}


# ============================================================================
# STUDENT ENDPOINTS
# ============================================================================

@classroom_router.get("/student/my-class")
async def get_student_class(student: dict = Depends(get_current_user)):
    """Học sinh xem thông tin lớp học hiện tại mà mình tham gia."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id, c.class_name, c.class_code, c.created_at, u.full_name as teacher_name, u.email as teacher_email, cm.joined_at
        FROM class_members cm
        JOIN classes c ON cm.class_id = c.id
        JOIN users u ON c.teacher_id = u.id
        WHERE cm.student_id = ?
    """, (student["id"],))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"has_class": False}

    return {
        "has_class": True,
        "class": dict(row)
    }


@classroom_router.post("/student/join")
async def join_class(req: JoinClassRequest, student: dict = Depends(get_current_user)):
    """Học sinh nhập mã lớp để tham gia lớp học."""
    code = req.class_code.strip().upper()
    if not code:
        raise HTTPException(status_code=400, detail="Vui lòng nhập mã lớp.")

    conn = get_connection()
    cursor = conn.cursor()

    # Tìm lớp theo mã code
    cursor.execute("""
        SELECT c.id, c.class_name, c.class_code, u.full_name as teacher_name
        FROM classes c
        JOIN users u ON c.teacher_id = u.id
        WHERE c.class_code = ?
    """, (code,))
    cls = cursor.fetchone()

    if not cls:
        conn.close()
        raise HTTPException(status_code=404, detail="Mã lớp không hợp lệ hoặc không tồn tại. Vui lòng kiểm tra lại với giáo viên.")

    class_id = cls["id"]

    # Kiểm tra học sinh đã tham gia lớp này chưa
    cursor.execute("SELECT id FROM class_members WHERE class_id = ? AND student_id = ?", (class_id, student["id"]))
    if cursor.fetchone():
        conn.close()
        return {
            "message": f"Bạn đã ở trong lớp '{cls['class_name']}' rồi!",
            "class": dict(cls)
        }

    # Nếu đang ở lớp khác, tự động chuyển sang lớp mới
    cursor.execute("DELETE FROM class_members WHERE student_id = ?", (student["id"],))
    cursor.execute("""
        INSERT INTO class_members (class_id, student_id)
        VALUES (?, ?)
    """, (class_id, student["id"]))

    conn.commit()
    conn.close()

    return {
        "message": f"🎉 Chúc mừng! Bạn đã tham gia thành công lớp '{cls['class_name']}' của giáo viên {cls['teacher_name']}!",
        "class": dict(cls)
    }


@classroom_router.post("/student/leave")
async def leave_class(student: dict = Depends(get_current_user)):
    """Học sinh rời khỏi lớp học hiện tại."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM class_members WHERE student_id = ?", (student["id"],))
    conn.commit()
    conn.close()
    return {"message": "Đã rời lớp học."}


@classroom_router.get("/student/assignments")
async def get_student_assignments(student: dict = Depends(get_current_user)):
    """Học sinh lấy danh sách bài tập được giáo viên lớp mình giao."""
    conn = get_connection()
    cursor = conn.cursor()

    # Lấy class_id của học sinh
    cursor.execute("SELECT class_id FROM class_members WHERE student_id = ?", (student["id"],))
    cm = cursor.fetchone()
    if not cm:
        conn.close()
        return {"in_class": False, "assignments": []}

    class_id = cm["class_id"]
    cursor.execute("""
        SELECT ca.id, ca.title, ca.description, ca.time_limit, ca.deadline, ca.created_at,
            (SELECT MAX(score) FROM assignment_submissions WHERE assignment_id = ca.id AND student_id = ?) as best_score,
            (SELECT COUNT(*) FROM assignment_submissions WHERE assignment_id = ca.id AND student_id = ?) as attempts
        FROM class_assignments ca
        WHERE ca.class_id = ?
        ORDER BY ca.created_at DESC
    """, (student["id"], student["id"], class_id))

    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        d["has_submitted"] = (d["attempts"] or 0) > 0
        d["is_ac"] = (d["best_score"] is not None and d["best_score"] > 0)
        result.append(d)

    return {
        "in_class": True,
        "assignments": result
    }


@classroom_router.get("/student/assignment/{assignment_id}")
async def get_assignment_detail(assignment_id: int, student: dict = Depends(get_current_user)):
    """Lấy chi tiết một bài tập giáo viên giao để hiển thị lên panel đề bài."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ca.*, c.class_name, u.full_name as teacher_name
        FROM class_assignments ca
        JOIN classes c ON ca.class_id = c.id
        JOIN users u ON ca.teacher_id = u.id
        WHERE ca.id = ?
    """, (assignment_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Bài tập không tồn tại.")

    data = dict(row)
    try:
        tcs = json.loads(data["test_cases_json"])
        data["total_tests"] = len(tcs)
        # Chỉ hiển thị 1-2 test mẫu cho học sinh xem ví dụ
        data["sample_tests"] = tcs[:2]
    except Exception:
        data["total_tests"] = 0
        data["sample_tests"] = []

    return data


@classroom_router.post("/student/assignment/{assignment_id}/submit")
async def submit_assignment_code(assignment_id: int, req: SubmitAssignmentRequest, student: dict = Depends(get_current_user)):
    """Chấm bài tập giáo viên giao: chạy với bộ test của bài tập + AI Mentor nhận xét."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM class_assignments WHERE id = ?", (assignment_id,))
    assignment = cursor.fetchone()
    conn.close()

    if not assignment:
        raise HTTPException(status_code=404, detail="Bài tập không tồn tại.")

    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code không được rỗng.")

    # 1. Lấy test cases
    try:
        test_cases = json.loads(assignment["test_cases_json"])
    except Exception:
        raise HTTPException(status_code=500, detail="Dữ liệu test cases bị lỗi.")

    if not test_cases:
        raise HTTPException(status_code=400, detail="Bài tập chưa có test cases.")

    # 2. Chấm code
    time_limit = assignment["time_limit"] or 1.0
    judge_result = judge_submission(
        student_code=req.code,
        test_cases=test_cases,
        time_limit=time_limit
    )

    # 3. AI Mentor nhận xét
    api_key = (req.api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip() or get_setting("api_key", "").strip()
    model_name = (req.model_name or "").strip() or os.environ.get("GEMINI_MODEL", "").strip() or get_setting("model_name", "").strip() or "gemini-3.5-flash-lite"

    try:
        ai_feedback = analyze_student_code(
            api_key=api_key,
            model_name=model_name,
            problem_desc=f"# {assignment['title']}\n\n{assignment['description']}",
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
        ai_feedback = f"⚠️ AI Mentor phản hồi: {str(e)}"

    # 4. Lưu bài nộp vào DB
    conn = get_connection()
    cursor = conn.cursor()
    status_str = "AC" if judge_result["score"] == judge_result["total"] else "WA"

    cursor.execute("""
        INSERT INTO assignment_submissions 
        (assignment_id, student_id, student_name, code, score, total_tests, status, results_json, ai_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        assignment_id,
        student["id"],
        student.get("full_name", "Học sinh"),
        req.code,
        judge_result["score"],
        judge_result["total"],
        status_str,
        json.dumps(judge_result["results"], ensure_ascii=False),
        ai_feedback
    ))
    conn.commit()
    conn.close()

    return {
        "score": judge_result["score"],
        "total": judge_result["total"],
        "status": status_str,
        "results": judge_result["results"],
        "ai_feedback": ai_feedback
    }

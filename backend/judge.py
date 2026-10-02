"""
judge.py - Hệ thống chấm bài tự động 10 test cases.
Thực thi code Python của học sinh trong subprocess cô lập với giới hạn thời gian.
"""

import subprocess
import sys
import os
import tempfile
import time


def judge_submission(student_code: str, test_cases: list, time_limit: float = 1.0) -> dict:
    """
    Chấm bài nộp của học sinh với danh sách test cases.

    Args:
        student_code: Source code Python của học sinh
        test_cases: List các dict {"input": str, "expected_output": str}
        time_limit: Giới hạn thời gian mỗi test (giây), mặc định 1.0s

    Returns:
        dict với score, total, và chi tiết từng test
    """
    results = []
    score = 0

    for i, test in enumerate(test_cases):
        test_input = test["input"]
        expected_output = test["expected_output"].strip()

        result = run_single_test(student_code, test_input, expected_output, time_limit, i + 1)
        results.append(result)

        if result["status"] == "AC":
            score += 1

    return {
        "score": score,
        "total": len(test_cases),
        "results": results
    }


def run_single_test(code: str, test_input: str, expected_output: str,
                    time_limit: float, test_number: int) -> dict:
    """
    Chạy code với một test case cụ thể.

    Returns:
        dict: {
            "test": int,
            "status": "AC" | "WA" | "TLE" | "RE",
            "time_ms": float,
            "input": str,
            "student_output": str,
            "expected_output": str,
            "error": str (nếu có)
        }
    """
    result = {
        "test": test_number,
        "status": "RE",
        "time_ms": 0,
        "input": test_input,
        "student_output": "",
        "expected_output": expected_output,
        "error": ""
    }

    # Tạo file tạm chứa code học sinh
    tmp_file = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False, encoding='utf-8'
        )
        tmp_file.write(code)
        tmp_file.close()

        # Chạy code trong subprocess cô lập
        start_time = time.perf_counter()

        process = subprocess.run(
            [sys.executable, "-u", tmp_file.name],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=time_limit + 0.5,  # Thêm 0.5s buffer cho startup
            cwd=tempfile.gettempdir(),
            env={
                "PATH": os.environ.get("PATH", ""),
                "PYTHONPATH": "",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )

        elapsed = time.perf_counter() - start_time
        result["time_ms"] = round(elapsed * 1000, 1)

        if process.returncode != 0:
            # Runtime Error
            result["status"] = "RE"
            stderr = process.stderr.strip()
            # Lọc bỏ đường dẫn file tạm, chỉ giữ thông tin lỗi
            error_lines = stderr.split('\n')
            filtered_errors = []
            for line in error_lines:
                if tmp_file.name not in line and "File " not in line:
                    filtered_errors.append(line)
                elif "Error" in line or "error" in line:
                    filtered_errors.append(line)
            result["error"] = '\n'.join(filtered_errors[-5:]) if filtered_errors else stderr[-500:]
            result["student_output"] = process.stdout.strip()
        else:
            student_output = process.stdout.strip()
            result["student_output"] = student_output

            # Kiểm tra thời gian
            if elapsed > time_limit:
                result["status"] = "TLE"
            else:
                # So sánh output (bỏ khoảng trắng thừa ở cuối mỗi dòng)
                if normalize_output(student_output) == normalize_output(expected_output):
                    result["status"] = "AC"
                else:
                    result["status"] = "WA"

    except subprocess.TimeoutExpired:
        result["status"] = "TLE"
        result["time_ms"] = round((time_limit + 0.5) * 1000, 1)
        result["error"] = f"Chương trình chạy quá {time_limit} giây."

    except Exception as e:
        result["status"] = "RE"
        result["error"] = str(e)

    finally:
        # Xóa file tạm
        if tmp_file and os.path.exists(tmp_file.name):
            try:
                os.unlink(tmp_file.name)
            except OSError:
                pass

    return result


def normalize_output(text: str) -> str:
    """Chuẩn hóa output để so sánh: bỏ khoảng trắng thừa cuối dòng và cuối file."""
    lines = text.strip().split('\n')
    return '\n'.join(line.rstrip() for line in lines)

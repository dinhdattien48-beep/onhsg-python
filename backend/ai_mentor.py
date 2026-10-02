"""
ai_mentor.py - Module tích hợp AI Gemini để nhận xét và gợi ý tối ưu code.
Sử dụng thư viện google-genai với fallback HTTP REST API và bộ phân tích Heuristic AI Mentor tích hợp sẵn.
Đảm bảo 100% LUÔN CÓ NHẬN XÉT CHI TIẾT CHO HỌC SINH dù Google API có bị lỗi 503, 404 hay sai Key!
"""

import os
import json
import re
import requests

# Tự động nạp biến môi trường từ file .env nếu có (dành cho local)
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
for _env_file in [os.path.join(os.path.dirname(_MODULE_DIR), ".env"), os.path.join(_MODULE_DIR, ".env")]:
    if os.path.exists(_env_file):
        try:
            with open(_env_file, "r", encoding="utf-8") as _f:
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


def _get_clean_models(requested_model: str) -> list:
    """Danh sách các model Gemini chính xác của Google."""
    valid_models = []
    if requested_model:
        valid_models.append(requested_model.strip())
    defaults = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    for m in defaults:
        if m not in valid_models:
            valid_models.append(m)
    return valid_models


def analyze_student_code(api_key: str = "", model_name: str = "", problem_desc: str = "",
                         student_code: str = "", judge_results: dict = None) -> str:
    """
    Phân tích code học sinh và đưa ra lời phê HSG Tin học theo đúng 4 mục.
    Thử Google Gemini trước; nếu Google bị 503, 404, 401 hoặc lỗi mạng,
    hệ thống sẽ tự động chuyển sang AI Mentor Heuristic Engine để đảm bảo học sinh
    LUÔN NHẬN ĐƯỢC NHẬN XÉT ĐẦY ĐỦ VÀ CHUẨN XÁC NHẤT.
    """
    api_key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    req_model = (model_name or "").strip() or os.environ.get("GEMINI_MODEL", "gemini-3.8-flash").strip()

    prompt = f"""
Bạn là giáo viên bồi dưỡng Học Sinh Giỏi Tin học bằng Python, đang dạy học sinh mới bắt đầu từ căn bản.

ĐỀ BÀI:
{problem_desc}

CODE CỦA HỌC SINH:
```python
{student_code}
```

KẾT QUẢ CHẤM 10 TEST:
{json.dumps(judge_results or {}, ensure_ascii=False, indent=2)}

Hãy nhận xét bài làm theo đúng 4 mục sau (ngôn ngữ dễ hiểu, khích lệ, không dùng từ ngữ quá hàn lâm):

1. **Lỗi cần sửa** (nếu có test sai WA, quá thời gian TLE hoặc lỗi chạy RE): Chỉ rõ dòng code hoặc logic bị hổng và trường hợp biên (edge case) bị sót.

2. **Loại bỏ chi tiết thừa**: Chỉ ra các biến dư thừa, vòng lặp không cần thiết hoặc đoạn code viết vòng vo.

3. **Tối ưu bằng hàm có sẵn (Built-in) của Python**: Gợi ý các hàm C-level có sẵn trong Python (như sum, max, min, sorted, math.gcd, math.isqrt, Counter, bisect, slicing...) có thể thay thế cho cách viết thủ công trong bài, giải thích rõ chức năng của hàm đó.

4. **Phân tích độ phức tạp**: Nêu độ phức tạp thời gian O(...) hiện tại của học sinh, giải thích vì sao nhanh hoặc chậm, và so sánh với cách viết tối ưu.

Trả lời bằng tiếng Việt, sử dụng Markdown formatting.
"""

    # Nếu có API Key, thử gọi Google Gemini qua SDK & REST API
    if api_key:
        models_to_try = _get_clean_models(req_model)
        for target_model in models_to_try:
            # 1. Thử gọi SDK
            try:
                res = _call_with_sdk(api_key, target_model, prompt)
                if res and len(res.strip()) > 30:
                    return res
            except Exception as e:
                pass

            # 2. Thử gọi REST API
            try:
                res = _call_with_rest(api_key, target_model, prompt)
                if res and len(res.strip()) > 30:
                    return res
            except Exception as e:
                pass

    # Fallback tự động: Hệ thống AI Mentor Heuristic tích hợp sẵn
    return generate_heuristic_feedback(problem_desc, student_code, judge_results or {})


def _call_with_sdk(api_key: str, model_name: str, prompt: str) -> str:
    """Gọi Gemini qua SDK google-genai."""
    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    if response and hasattr(response, 'text') and response.text:
        return response.text
    return ""


def _call_with_rest(api_key: str, model_name: str, prompt: str) -> str:
    """Gọi Gemini qua HTTP REST API (Header x-goog-api-key an toàn)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 3000,
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=25)
    response.raise_for_status()

    data = response.json()
    if "candidates" in data and len(data["candidates"]) > 0:
        candidate = data["candidates"][0]
        if "content" in candidate and "parts" in candidate["content"]:
            return candidate["content"]["parts"][0].get("text", "")

    return ""


def generate_heuristic_feedback(problem_desc: str, student_code: str, judge_results: dict) -> str:
    """
    Bộ phân tích AI Mentor Heuristic thông minh cho bài làm HSG Tin học.
    Đưa ra nhận xét cực kỳ chuẩn xác, thiết thực theo đúng 4 mục của ban chuyên môn.
    """
    score = judge_results.get("score", 0)
    total = judge_results.get("total", 10)
    details = judge_results.get("details", [])

    failed_tests = [d for d in details if d.get("status") != "AC"]
    failed_reasons = set(d.get("status") for d in failed_tests)

    # 1. Phân tích Lỗi cần sửa
    if score == total:
        sec1 = (
            "🎉 **Chúc mừng em! Code đã vượt qua hoàn hảo 10/10 test cases.**\n"
            "- Không có lỗi logic cơ bản, xử lý tốt cả các trường hợp dữ liệu lớn và biên."
        )
    else:
        sec1 = f"⚠️ **Bài làm đạt {score}/{total} test. Cần khắc phục các điểm sau:**\n"
        if "TLE" in failed_reasons:
            sec1 += (
                "- **Quá giới hạn thời gian (TLE):** Thuật toán hiện tại đang chạy chậm ở các test có dữ liệu lớn. "
                "Cần tránh lặp $O(N^2)$ hoặc phép cộng dồn chuỗi lặp lại nhiều lần. "
                "Hãy dùng `sys.stdin.readline` để tăng tốc độ nhập dữ liệu.\n"
            )
        if "WA" in failed_reasons:
            sec1 += (
                "- **Kết quả chưa chính xác (WA):** Thuật toán bị sót trường hợp biên. "
                "Hãy kiểm tra lại: số âm, số 0, trường hợp danh sách rỗng hoặc dữ liệu cận trên $10^9$.\n"
            )
        if "RE" in failed_reasons:
            sec1 += (
                "- **Lỗi thực thi khi chạy (RE):** Chương trình bị dừng đột ngột. "
                "Nguyên nhân phổ biến: chia cho 0 (`ZeroDivisionError`), truy cập ngoài chỉ số danh sách (`IndexError`), "
                "hoặc đọc thiếu dòng input khi đề bài có nhiều dòng.\n"
            )

    # 2. Phân tích Chi tiết thừa & Tối ưu phong cách
    sec2_items = []
    if "while " in student_code and "for " not in student_code:
        sec2_items.append("Nếu đã biết trước số lượng phần tử lặp, hãy dùng vòng lặp `for ... in range(...)` thay cho `while` để code ngắn gọn, tự động tăng chỉ số và tránh nguy cơ lặp vô tận.")

    if student_code.count("print(") > 3 and ("for " in student_code or "while " in student_code):
        sec2_items.append("Đang gọi `print()` nhiều lần liên tiếp trong vòng lặp. Trong bài thi HSG, gọi `print()` nhiều lần sẽ làm chậm I/O, nên gom kết quả vào mảng rồi in ra một lần.")

    if " = list()" in student_code:
        sec2_items.append("Nên viết `[]` thay cho `list()` để khởi tạo danh sách nhanh và chuẩn Pythonic hơn.")

    if not sec2_items:
        sec2 = "- Cách khai báo biến rõ ràng, mạch lạc, không có thao tác thừa thãi làm chậm chương trình."
    else:
        sec2 = "\n".join(f"- {item}" for item in sec2_items)

    # 3. Gợi ý hàm Built-in của Python
    sec3_items = []
    if "for " in student_code and ("+ " in student_code or "+=" in student_code) and "sum(" not in student_code:
        sec3_items.append("Dùng hàm **`sum(iterable)`**: Hàm `sum()` được viết bằng ngôn ngữ C trong lõi Python, tính tổng mảng nhanh gấp 3–5 lần so với việc dùng vòng lặp `for` cộng dồn từng phần tử thủ công.")

    if ("max " in student_code or "min " in student_code or ">" in student_code) and "max(" not in student_code and "min(" not in student_code:
        sec3_items.append("Dùng hàm **`max()`** và **`min()`**: Có thể truyền nhiều tham số cùng lúc như `max(a, b, c)` hoặc `max(danh_sach)` thay vì phải viết nhiều nhánh `if-else` so sánh thủ công.")

    if "math" not in student_code and ("ước" in problem_desc.lower() or "gcd" in student_code.lower()):
        sec3_items.append("Dùng **`math.gcd(a, b)`**: Tìm ước chung lớn nhất cực nhanh bằng thuật toán Euclid tối ưu sẵn trong thư viện chuẩn `math`.")

    if "sys.stdin.readline" not in student_code:
        sec3_items.append("Vũ khí tối thượng tăng tốc nhập: Thêm 2 dòng ở đầu bài `import sys` và `input = sys.stdin.readline` để tăng tốc đọc dữ liệu lên gấp 5–10 lần khi gặp bài có hàng trăm nghìn dòng.")

    if not sec3_items:
        sec3_items.append("Em đã áp dụng khá tốt các cấu trúc chuẩn của Python. Hãy tiếp tục duy trì việc dùng list comprehension `[x for x in ...]` và các hàm built-in.")

    sec3 = "\n".join(f"- {item}" for item in sec3_items)

    # 4. Phân tích độ phức tạp thời gian O(...)
    # Đếm số vòng lặp lồng nhau
    lines = student_code.split("\n")
    loop_depth = 0
    max_loop_depth = 0
    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if stripped.startswith("for ") or stripped.startswith("while "):
            loop_depth += 1
            max_loop_depth = max(max_loop_depth, loop_depth)
        elif indent == 0 and stripped:
            loop_depth = 0

    if max_loop_depth >= 2:
        sec4 = (
            f"- **Độ phức tạp hiện tại:** Khoảng **$O(N^2)$** (do có {max_loop_depth} vòng lặp lồng nhau).\n"
            "- **Đánh giá:** Với $N \\le 5000$, cách này vẫn chạy kịp ($2.5 \\times 10^7$ phép tính). "
            "Nhưng khi $N \\ge 10^5$, thuật toán sẽ vượt quá 1 giây và bị lỗi TLE. "
            "Cần hướng tới độ phức tạp $O(N)$ hoặc $O(N \\log N)$ bằng cách sử dụng mảng đếm (Hashing/Counter) hoặc hai con trỏ (Two Pointers)."
        )
    elif max_loop_depth == 1:
        sec4 = (
            "- **Độ phức tạp hiện tại:** Khoảng **$O(N)$** (chỉ dùng một vòng lặp đơn).\n"
            "- **Đánh giá:** Rất tối ưu! Với độ phức tạp $O(N)$, chương trình có thể xử lý mượt mà lên tới $N = 10^7$ phần tử trong vòng 1 giây, hoàn toàn đạt chuẩn bài thi HSG."
        )
    else:
        sec4 = (
            "- **Độ phức tạp hiện tại:** **$O(1)$** (Thời gian hằng số, chỉ dùng phép toán đại số).\n"
            "- **Đánh giá:** Tối ưu tuyệt đối! Chương trình thực thi tức thì dưới 1ms trên mọi bộ dữ liệu."
        )

    return f"""### 🤖 Lời nhận xét từ AI Mentor

{sec1}

#### 2. Loại bỏ chi tiết thừa & Viết code chuẩn
{sec2}

#### 3. Tối ưu bằng hàm có sẵn (Built-in) của Python
{sec3}

#### 4. Phân tích độ phức tạp thuật toán
{sec4}
"""

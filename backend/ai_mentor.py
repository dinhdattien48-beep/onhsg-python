"""
ai_mentor.py - Module tích hợp AI Gemini để nhận xét và gợi ý tối ưu code.
Sử dụng thư viện google-genai (MỚI) với fallback sang HTTP REST API.
"""

import os
import json
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


def analyze_student_code(api_key: str = "", model_name: str = "", problem_desc: str = "",
                         student_code: str = "", judge_results: dict = None) -> str:
    """
    Gọi Gemini AI để phân tích và nhận xét code của học sinh.
    Thử SDK google-genai trước, nếu lỗi thì fallback sang REST API.
    Nếu không truyền api_key hoặc model_name thì tự động lấy từ biến môi trường:
    - GEMINI_API_KEY
    - GEMINI_MODEL (mặc định: 'gemini-3.8-flash')
    """
    # Lấy API Key từ tham số truyền vào hoặc biến môi trường server
    api_key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    model_name = (model_name or "").strip() or os.environ.get("GEMINI_MODEL", "gemini-3.8-flash").strip()

    if not api_key:
        return (
            "⚠️ **Chưa cấu hình Gemini API Key**\n\n"
            "Vui lòng thiết lập biến môi trường `GEMINI_API_KEY` trên máy chủ để kích hoạt AI Mentor nhận xét code tự động."
        )

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

    # Thử dùng SDK google-genai trước
    try:
        return _call_with_sdk(api_key, model_name, prompt)
    except Exception as sdk_error:
        print(f"[AI Mentor] SDK google-genai lỗi: {sdk_error}")
        print("[AI Mentor] Chuyển sang gọi REST API...")
        try:
            return _call_with_rest(api_key, model_name, prompt)
        except Exception as rest_error:
            print(f"[AI Mentor] REST API cũng lỗi: {rest_error}")
            return (
                "⚠️ **Không thể kết nối AI Mentor**\n\n"
                f"Lỗi SDK: {str(sdk_error)}\n\n"
                f"Lỗi REST: {str(rest_error)}\n\n"
                "Hãy kiểm tra lại biến môi trường GEMINI_API_KEY và GEMINI_MODEL trên server."
            )


def _call_with_sdk(api_key: str, model_name: str, prompt: str) -> str:
    """Gọi Gemini qua SDK google-genai (thư viện mới nhất)."""
    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return response.text


def _call_with_rest(api_key: str, model_name: str, prompt: str) -> str:
    """Fallback: Gọi Gemini qua HTTP REST API trực tiếp."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "key": api_key
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
            "maxOutputTokens": 4096,
        }
    }

    response = requests.post(url, headers=headers, params=params, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()

    if "candidates" in data and len(data["candidates"]) > 0:
        candidate = data["candidates"][0]
        if "content" in candidate and "parts" in candidate["content"]:
            return candidate["content"]["parts"][0].get("text", "Không có phản hồi.")

    return "Không nhận được phản hồi từ AI. Vui lòng thử lại."

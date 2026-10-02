"""
ai_mentor.py - Module tích hợp AI Gemini để nhận xét và gợi ý tối ưu code.
Sử dụng thư viện google-genai (MỚI) với fallback sang HTTP REST API.
Hỗ trợ cơ chế tự động chuyển model dự phòng (Model Cascade) khi model chính gặp lỗi 503 (quá tải) hoặc 404.
"""

import os
import json
import requests
import re

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


def _mask_secret(text: str, secret: str) -> str:
    """Che giấu chuỗi API key khỏi các log hoặc thông báo lỗi."""
    if not secret or len(secret) < 8:
        return text
    masked = secret[:6] + "..." + secret[-4:]
    return text.replace(secret, masked)


def _get_candidate_models(primary_model: str) -> list:
    """Tạo danh sách các model ưu tiên để tự động chuyển đổi khi model chính bị quá tải (503)."""
    candidates = []
    if primary_model:
        candidates.append(primary_model.strip())
    # Danh sách model dự phòng theo thứ tự tối ưu
    defaults = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    for m in defaults:
        if m not in candidates:
            candidates.append(m)
    return candidates


def analyze_student_code(api_key: str = "", model_name: str = "", problem_desc: str = "",
                         student_code: str = "", judge_results: dict = None) -> str:
    """
    Gọi Gemini AI để phân tích và nhận xét code của học sinh.
    Tự động thử các model ổn định nếu model chính bị quá tải (503 High Demand).
    """
    api_key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    primary_model = (model_name or "").strip() or os.environ.get("GEMINI_MODEL", "gemini-3.8-flash").strip()

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

    candidate_models = _get_candidate_models(primary_model)
    last_error = ""

    for target_model in candidate_models:
        # 1. Thử gọi bằng SDK google-genai
        try:
            return _call_with_sdk(api_key, target_model, prompt)
        except Exception as sdk_err:
            err_msg = str(sdk_err)
            print(f"[AI Mentor] SDK lỗi với model {target_model}: {err_msg[:120]}")
            last_error = err_msg

        # 2. Thử gọi bằng REST API trực tiếp
        try:
            return _call_with_rest(api_key, target_model, prompt)
        except Exception as rest_err:
            err_msg = str(rest_err)
            print(f"[AI Mentor] REST API lỗi với model {target_model}: {err_msg[:120]}")
            last_error = err_msg

        # Nếu lỗi 401 Unauthorized (sai key / key không hợp lệ) thì dừng ngay, không thử model khác
        if "401" in last_error or "UNAUTHENTICATED" in last_error:
            clean_err = _mask_secret(last_error, api_key)
            return (
                "⚠️ **Lỗi xác thực API Key (401 Unauthorized)**\n\n"
                f"- **Chi tiết:** {_mask_secret(last_error, api_key)}\n\n"
                "💡 **Cách khắc phục:**\n"
                "1. Hãy kiểm tra lại `GEMINI_API_KEY`. API Key chuẩn của Google AI Studio có dạng bắt đầu bằng `AIzaSy...`.\n"
                "2. Bạn có thể lấy Key miễn phí hoàn toàn tại: https://aistudio.google.com/apikey"
            )

    # Nếu tất cả model đều bị quá tải hoặc lỗi
    safe_error = _mask_secret(last_error, api_key)
    return (
        "⚠️ **Hệ thống AI của Google đang bị quá tải tạm thời (503 Service Unavailable)**\n\n"
        f"- Chi tiết từ Google: `{safe_error}`\n\n"
        "💡 **Cách khắc phục:**\n"
        "1. Sự cố máy chủ Google quá tải (Spike in demand) thường chỉ diễn ra trong vài chục giây, bạn hãy **bấm Nộp bài lại sau 30 giây**.\n"
        "2. Hoặc kiểm tra lại API Key lấy từ https://aistudio.google.com/apikey (chuẩn `AIzaSy...`)."
    )


def _call_with_sdk(api_key: str, model_name: str, prompt: str) -> str:
    """Gọi Gemini qua SDK google-genai (thư viện mới nhất)."""
    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    if response and hasattr(response, 'text') and response.text:
        return response.text
    return "Không nhận được phản hồi từ AI."


def _call_with_rest(api_key: str, model_name: str, prompt: str) -> str:
    """Fallback: Gọi Gemini qua HTTP REST API trực tiếp (bảo mật: truyền key qua header)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    # Truyền API Key qua header x-goog-api-key để không bị lộ trên URL query string
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
            "maxOutputTokens": 4096,
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()

    if "candidates" in data and len(data["candidates"]) > 0:
        candidate = data["candidates"][0]
        if "content" in candidate and "parts" in candidate["content"]:
            return candidate["content"]["parts"][0].get("text", "Không có phản hồi.")

    return "Không nhận được phản hồi từ AI. Vui lòng thử lại."

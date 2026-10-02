"""
ai_mentor.py - Module AI Mentor cho HSG Python.
- Gọi Google Gemini (SDK + REST fallback) với đề bài + code + kết quả chấm thật.
- Fallback Heuristic Engine đọc code thật để nhận xét cụ thể.
- Nếu điểm < 50%, tự động sinh code mẫu Python dùng biến tiếng Việt dễ hiểu.
"""

import os
import json
import re
import requests

# Tự động nạp file .env nếu có (dành cho local)
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
    """Danh sach model Gemini uu tien thu theo thu tu."""
    valid_models = []
    if requested_model:
        valid_models.append(requested_model.strip())
    for m in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
        if m not in valid_models:
            valid_models.append(m)
    return valid_models


def _kiem_tra_code_rong(code: str) -> bool:
    """Kiem tra xem code co thuc su co logic giai bai hay khong."""
    for dong in code.split("\n"):
        stripped = dong.strip()
        if (stripped and
                not stripped.startswith("#") and
                not stripped.startswith("import ") and
                not stripped.startswith("from ") and
                stripped not in ("input = sys.stdin.readline",
                                 "input=sys.stdin.readline",
                                 "# Viet code Python o day",
                                 "# Viết code Python ở đây")):
            return False
    return True


def analyze_student_code(api_key: str = "", model_name: str = "",
                          problem_desc: str = "", student_code: str = "",
                          judge_results: dict = None,
                          cached_sample_code: str = "") -> str:
    """
    Nhan xet bai lam hoc sinh dua vao de bai + code + ket qua cham.
    - cached_sample_code: code mau da luu tu truoc (khong sinh lai).
    - Phat hien code rong (chi co import, khong co logic) -> bao loi ngay.
    - Thu Google Gemini truoc; neu loi -> Heuristic Engine.
    """
    api_key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    req_model = (model_name or "").strip() or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()

    diem_dat = (judge_results or {}).get("score", 0)
    tong_test = (judge_results or {}).get("total", 10)
    ty_le_dung = diem_dat / tong_test if tong_test > 0 else 0

    # Uu tien phat hien code rong - khong can goi AI
    if _kiem_tra_code_rong(student_code):
        phan_code_mau = _format_code_mau_block(cached_sample_code)
        return f"""### 🤖 Lời nhận xét từ AI Mentor

#### 1. Lỗi cần sửa
- **Code chưa có logic giải bài:** Em chỉ có các dòng `import` nhưng chưa viết bất kỳ logic nào để giải quyết yêu cầu đề bài.
- Hãy đọc kỹ **Đề bài** rồi suy nghĩ: *Dữ liệu đầu vào là gì? Kết quả cần in ra là gì? Cần tính toán gì để ra kết quả?*
- Bước tiếp theo: đọc input (`n = int(input())`), xử lý, rồi in output.

#### 2. Loại bỏ chi tiết thừa & Viết code chuẩn
- Chưa có code để nhận xét. Hãy viết logic giải bài trước nhé!

#### 3. Tối ưu bằng hàm có sẵn (Built-in) của Python
- `sum()`, `max()`, `min()`, `sorted()` là các hàm hay gặp trong HSG. Sẽ gợi ý cụ thể sau khi em có code.

#### 4. Phân tích độ phức tạp thuật toán
- Chưa có code để phân tích. Viết solution trước, AI Mentor sẽ nhận xét ngay!
{phan_code_mau}"""

    # Code mau cho prompt Gemini (chi yeu cau sinh khi chua co cache)
    yeu_cau_sinh_code_mau = ""
    if ty_le_dung < 0.5 and not cached_sample_code:
        yeu_cau_sinh_code_mau = """
5. **Code Mau Goi Y** (vi bai dat duoi 50%): Viet 1 doan code Python hoan chinh giai bai tren,
   su dung ten bien tieng Viet khong dau (vi du: so_luong, tong_gia_tri, danh_sach_phan_tu)
   de hoc sinh de hieu y nghia tung bien. Them comment tieng Viet giai thich tung buoc.
   Format: dat code trong khoi ```python ... ```.
"""

    prompt = f"""Ban la giao vien boi duong Hoc Sinh Gioi Tin hoc bang Python, dang day hoc sinh lop 8-10 moi bat dau tu can ban.

=== DE BAI ===
{problem_desc}

=== CODE BAI LAM CUA HOC SINH ===
```python
{student_code}
```

=== KET QUA CHAM ({diem_dat}/{tong_test} test dung) ===
{json.dumps(judge_results or {}, ensure_ascii=False, indent=2)}

Hay doc KY ca DE BAI va CODE CUA HOC SINH o tren roi nhan xet theo {4 + (1 if yeu_cau_sinh_code_mau else 0)} muc.
Viet nhan xet bang tieng Viet co dau, chi doc CODE THAT cua hoc sinh - khong doan mo:

1. **Loi can sua** - So sanh truc tiep code hoc sinh voi yeu cau de bai:
   - Dong code nao sai / thieu logic gi so voi yeu cau de bai.
   - Truong hop bien nao bi bo sot (so am, so 0, list rong, gia tri cuc lon...).
   - Neu co test WA/TLE/RE, giai thich nguyen nhan cu the trong code.
   - Neu dung het 10/10, khen ngoi cu the diem hay trong code.

2. **Loai bo chi tiet thua** - Chi ra bien du, vong lap khong can thiet hoac code vong vo.

3. **Toi uu bang ham Built-in Python** - Goi y ham thay the code thu cong (sum, max, sorted, Counter, math.gcd...).

4. **Phan tich do phuc tap** - Neu O(...) hien tai, giai thich vi sao nhanh/cham.
{yeu_cau_sinh_code_mau}
Tra loi bang tieng Viet co dau, dung Markdown formatting."""

    # Neu co API Key -> thu Gemini
    if api_key:
        models_to_try = _get_clean_models(req_model)
        for target_model in models_to_try:
            try:
                ket_qua = _call_with_sdk(api_key, target_model, prompt)
                if ket_qua and len(ket_qua.strip()) > 50:
                    # Neu da co cached_sample, gan them vao cuoi neu Gemini chua sinh
                    if ty_le_dung < 0.5 and cached_sample_code and "```python" not in ket_qua:
                        ket_qua += "\n" + _format_code_mau_block(cached_sample_code)
                    return ket_qua
            except Exception:
                pass
            try:
                ket_qua = _call_with_rest(api_key, target_model, prompt)
                if ket_qua and len(ket_qua.strip()) > 50:
                    if ty_le_dung < 0.5 and cached_sample_code and "```python" not in ket_qua:
                        ket_qua += "\n" + _format_code_mau_block(cached_sample_code)
                    return ket_qua
            except Exception:
                pass

    # Fallback: Heuristic Engine doc code that
    return generate_heuristic_feedback(
        problem_desc, student_code, judge_results or {},
        cached_sample_code=cached_sample_code
    )


def _format_code_mau_block(cached_sample_code: str) -> str:
    """Dinh dang phan code mau de hien thi."""
    if not cached_sample_code:
        return ""
    return f"""
#### 5. Code Mẫu Gợi Ý (Tham khảo để hiểu hướng giải)

> **Đây là gợi ý tham khảo** - Em hãy đọc hiểu rồi tự viết lại theo cách riêng của mình nhé!

```python
{cached_sample_code}
```"""


def _call_with_sdk(api_key: str, model_name: str, prompt: str) -> str:
    """Goi Gemini qua SDK google-genai."""
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model_name, contents=prompt)
    if response and hasattr(response, "text") and response.text:
        return response.text
    return ""


def _call_with_rest(api_key: str, model_name: str, prompt: str) -> str:
    """Goi Gemini qua HTTP REST API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4000},
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    if "candidates" in data and data["candidates"]:
        candidate = data["candidates"][0]
        if "content" in candidate and "parts" in candidate["content"]:
            return candidate["content"]["parts"][0].get("text", "")
    return ""


# ============================================================================
# HEURISTIC ENGINE - DOC CODE THAT, NHAN XET CU THE
# ============================================================================

def generate_heuristic_feedback(problem_desc: str, student_code: str,
                                 judge_results: dict,
                                 cached_sample_code: str = "") -> str:
    """
    AI Mentor Heuristic: doc code hoc sinh that va de bai de nhan xet cu the.
    Khong doan mo - chi nhan xet nhung gi thuc su co trong code.
    """
    diem_dat = judge_results.get("score", 0)
    tong_test = judge_results.get("total", 10)
    chi_tiet = judge_results.get("details", [])

    test_sai = [d for d in chi_tiet if d.get("status") != "AC"]
    ly_do_sai = set(d.get("status") for d in test_sai)

    # 1. Phan tich loi
    if diem_dat == tong_test:
        muc_1 = (
            "Chúc mừng em! Code vượt qua hoàn hảo 10/10 test cases.\n"
            + _nhan_xet_code_tot(student_code)
        )
    else:
        muc_1 = f"Bài làm đạt {diem_dat}/{tong_test} test. Phân tích lỗi:\n"
        muc_1 += _nhan_xet_loi_cu_the(student_code, problem_desc, ly_do_sai)

    # 2. Chi tiet thua
    muc_2_items = _phat_hien_chi_tiet_thua(student_code)
    muc_2 = "\n".join(f"- {item}" for item in muc_2_items) if muc_2_items else \
        "- Cách khai báo biến rõ ràng, mạch lạc, không có thao tác thừa thãi."

    # 3. Built-in
    muc_3_items = _goi_y_builtin(student_code, problem_desc)
    muc_3 = "\n".join(f"- {item}" for item in muc_3_items)

    # 4. Do phuc tap
    muc_4 = _phan_tich_do_phuc_tap(student_code)

    # 5. Code mau: uu tien dung cached, chi sinh moi neu chua co cache
    ty_le = diem_dat / tong_test if tong_test > 0 else 1
    muc_5 = ""
    if ty_le < 0.5:
        if cached_sample_code:
            # Dung code mau da cache (khong sinh lai)
            muc_5 = _format_code_mau_block(cached_sample_code)
        else:
            # Sinh code mau lan dau (se duoc luu boi main.py)
            code_mau_moi = _sinh_code_mau(problem_desc, student_code)
            if code_mau_moi:
                muc_5 = _format_code_mau_block(code_mau_moi)

    return f"""### 🤖 Lời nhận xét từ AI Mentor

#### 1. Lỗi cần sửa
{muc_1}

#### 2. Loại bỏ chi tiết thừa & Viết code chuẩn
{muc_2}

#### 3. Tối ưu bằng hàm có sẵn (Built-in) của Python
{muc_3}

#### 4. Phân tích độ phức tạp thuật toán
{muc_4}
{muc_5}"""


def _nhan_xet_code_tot(student_code: str) -> str:
    diem_tot = []
    if "sys.stdin" in student_code:
        diem_tot.append("Em đã dùng `sys.stdin.readline` - tăng tốc nhập dữ liệu chuẩn HSG.")
    if "def " in student_code:
        diem_tot.append("Em đã tách code thành hàm (`def`) - rất chuyên nghiệp và dễ debug.")
    if "sum(" in student_code or "max(" in student_code or "min(" in student_code:
        diem_tot.append("Em đã dùng hàm built-in của Python (`sum/max/min`) - thực hành chuẩn thi HSG.")
    if not diem_tot:
        diem_tot.append("Code chính xác, xử lý đúng yêu cầu đề bài.")
    return "\n".join(f"- {d}" for d in diem_tot)


def _nhan_xet_loi_cu_the(student_code: str, problem_desc: str, ly_do_sai: set) -> str:
    cac_loi = []

    if "TLE" in ly_do_sai:
        so_vong_lap = student_code.count("for ") + student_code.count("while ")
        if so_vong_lap >= 2:
            cac_loi.append(
                f"**Quá giới hạn thời gian (TLE):** Em đang dùng nhiều vòng lặp lồng nhau "
                f"(phát hiện {so_vong_lap} vòng lặp trong code). "
                "Với dữ liệu lớn, $O(N^2)$ sẽ vượt quá 1 giây. "
                "Hãy thử dùng `sum()`, `Counter`, hoặc sắp xếp một lần rồi dùng hai con trỏ."
            )
        else:
            cac_loi.append(
                "**Quá giới hạn thời gian (TLE):** Phép tính trong vòng lặp đang quá nặng. "
                "Thêm `import sys; input = sys.stdin.readline` và kiểm tra có thể "
                "dùng hàm built-in thay thế không."
            )

    if "WA" in ly_do_sai:
        thieu_bien = []
        if student_code.count("if ") < 2:
            thieu_bien.append("kiểm tra điều kiện biên")
        mo_ta_bien = f" (có thể thiếu xử lý: {', '.join(thieu_bien)})" if thieu_bien else ""
        cac_loi.append(
            f"**Kết quả sai (WA){mo_ta_bien}:** Thuật toán bị sai ở một số trường hợp. "
            "Hãy test thử: n=0, n=1, tất cả phần tử bằng nhau, giá trị tối đa $10^9$."
        )

    if "RE" in ly_do_sai:
        nguyen_nhan = []
        if "/" in student_code:
            nguyen_nhan.append("`ZeroDivisionError` - có thể bị chia cho 0")
        if "[" in student_code and "]" in student_code:
            nguyen_nhan.append("`IndexError` - truy cập phần tử ngoài giới hạn mảng")
        mo_ta = "; ".join(nguyen_nhan) if nguyen_nhan else "chia cho 0 hoặc truy cập mảng ngoài biên"
        cac_loi.append(
            f"**Lỗi thực thi (RE):** Nguyên nhân có thể trong code: {mo_ta}. "
            "Thêm điều kiện kiểm tra trước khi tính toán."
        )

    if not cac_loi:
        cac_loi.append("Chưa xác định được lỗi cụ thể - hãy thử chạy thử từng test nhỏ.")

    return "\n".join(f"- {loi}" for loi in cac_loi)


def _phat_hien_chi_tiet_thua(student_code: str) -> list:
    items = []

    if "while " in student_code and "for " not in student_code:
        items.append(
            "Nếu đã biết trước số vòng lặp, dùng `for i in range(n)` thay `while` "
            "để code ngắn hơn và tránh lặp vô tận."
        )

    cac_dong = student_code.split("\n")
    print_trong_vong_lap = 0
    dang_trong_vong = False
    for dong in cac_dong:
        stripped = dong.strip()
        if stripped.startswith("for ") or stripped.startswith("while "):
            dang_trong_vong = True
        elif len(dong) - len(dong.lstrip()) == 0 and stripped and not stripped.startswith("#"):
            dang_trong_vong = False
        if dang_trong_vong and "print(" in stripped:
            print_trong_vong_lap += 1

    if print_trong_vong_lap >= 3:
        items.append(
            f"Em đang gọi `print()` ~{print_trong_vong_lap} lần trong vòng lặp. "
            "Hãy gom kết quả vào list rồi dùng `print('\\n'.join(ket_qua))` để in một lần - nhanh hơn nhiều."
        )

    if " = list()" in student_code:
        items.append("Dùng `[]` thay `list()` để khởi tạo list - ngắn hơn và chuẩn Pythonic.")

    return items


def _goi_y_builtin(student_code: str, problem_desc: str) -> list:
    items = []
    de_lower = problem_desc.lower()

    if "+=" in student_code and ("for " in student_code or "while " in student_code) and "sum(" not in student_code:
        items.append(
            "**`sum(iterable)`**: Em đang cộng dồn thủ công trong vòng lặp. "
            "Hàm `sum()` viết bằng C, nhanh gấp 3-5 lần: `tong = sum(danh_sach)`"
        )

    if (">" in student_code or "<" in student_code) and "max(" not in student_code and "min(" not in student_code:
        if re.search(r'if .+[><].+:', student_code):
            items.append(
                "**`max()` / `min()`**: Thay vì so sánh thủ công bằng `if`, "
                "dùng `max(a, b)` hoặc `max(danh_sach)` - ngắn gọn hơn rất nhiều."
            )

    if ("uoc" in de_lower or "gcd" in student_code.lower() or "boi" in de_lower) and "math.gcd" not in student_code:
        items.append(
            "**`math.gcd(a, b)`**: Tìm ước chung lớn nhất siêu nhanh: "
            "`import math; ket_qua = math.gcd(so_a, so_b)`."
        )

    if re.search(r'\w+\[.+\]\s*\+=\s*1', student_code) and "Counter" not in student_code:
        items.append(
            "**`Counter(iterable)`** từ `collections`: Đếm tần suất phần tử cực nhanh: "
            "`from collections import Counter; tan_suat = Counter(danh_sach)`."
        )

    if "sys.stdin" not in student_code:
        items.append(
            "**Tăng tốc nhập liệu**: Thêm 2 dòng đầu bài: `import sys` và `input = sys.stdin.readline` "
            "- tăng tốc đọc dữ liệu gấp 5-10 lần khi có nhiều dòng nhập."
        )

    if not items:
        items.append(
            "Em đã dùng khá tốt các cấu trúc chuẩn Python. "
            "Tiếp tục thực hành `list comprehension` và các hàm built-in nhé!"
        )

    return items


def _phan_tich_do_phuc_tap(student_code: str) -> str:
    cac_dong = student_code.split("\n")
    do_sau_max = 0
    stack_indent = []

    for dong in cac_dong:
        stripped = dong.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(dong) - len(dong.lstrip(" "))
        if stripped.startswith("for ") or stripped.startswith("while "):
            while stack_indent and stack_indent[-1] >= indent:
                stack_indent.pop()
            stack_indent.append(indent)
            do_sau_max = max(do_sau_max, len(stack_indent))
        elif indent == 0 and stripped and not stripped.startswith("def ") and not stripped.startswith("class "):
            if not (stripped.startswith("for ") or stripped.startswith("while ")):
                stack_indent = []

    co_sort = "sorted(" in student_code or ".sort(" in student_code

    if do_sau_max >= 3:
        return (
            f"- **Độ phức tạp hiện tại:** Khoảng **$O(N^3)$** (có {do_sau_max} vòng lặp lồng nhau).\n"
            "- Nguy hiểm! Với $N \\ge 1000$, sẽ bị TLE ngay. Cần tái cấu trúc thuật toán."
        )
    elif do_sau_max == 2:
        return (
            "- **Độ phức tạp hiện tại:** Khoảng **$O(N^2)$** (2 vòng lặp lồng nhau).\n"
            "- Chấp nhận được với $N \\le 5000$, nhưng sẽ TLE khi $N \\ge 10^5$. "
            "Hãy thử dùng hai con trỏ hoặc Hashing để đạt $O(N)$."
        )
    elif do_sau_max == 1 and co_sort:
        return (
            "- **Độ phức tạp hiện tại:** Khoảng **$O(N \\log N)$** (1 vòng lặp + sắp xếp).\n"
            "- Rất tốt! Đủ nhanh với $N \\le 10^6$."
        )
    elif do_sau_max == 1:
        return (
            "- **Độ phức tạp hiện tại:** Khoảng **$O(N)$** (chỉ 1 vòng lặp đơn).\n"
            "- Xuất sắc! Xử lý được $N = 10^7$ trong 1 giây."
        )
    else:
        return (
            "- **Độ phức tạp hiện tại:** **$O(1)$** hoặc $O(\\log N)$.\n"
            "- Tối ưu tuyệt đối!"
        )


def _sinh_code_mau(problem_desc: str, student_code: str) -> str:
    """Sinh code mau Python dung bien tieng Viet khong dau dua tren de bai."""
    de_lower = problem_desc.lower()

    neu_nguyen_to = "nguyen to" in de_lower or "prime" in de_lower
    neu_uoc = "uoc chung" in de_lower or "gcd" in de_lower or "boi chung" in de_lower
    neu_sap_xep = "sap xep" in de_lower or "sort" in de_lower
    neu_tinh_tong = "tong" in de_lower or "sum" in de_lower
    neu_tim_max = "lon nhat" in de_lower or "maximum" in de_lower
    neu_tim_min = "nho nhat" in de_lower or "minimum" in de_lower
    neu_dem = "dem" in de_lower or "count" in de_lower or "so luong" in de_lower

    if neu_nguyen_to:
        return (
            "import sys\n"
            "input = sys.stdin.readline\n\n"
            "def kiem_tra_nguyen_to(so_can_kiem):\n"
            "    # So nho hon 2 khong phai nguyen to\n"
            "    if so_can_kiem < 2:\n"
            "        return False\n"
            "    # Kiem tra tu 2 den can bac hai\n"
            "    for uoc_chia in range(2, int(so_can_kiem**0.5) + 1):\n"
            "        if so_can_kiem % uoc_chia == 0:\n"
            "            return False\n"
            "    return True\n\n"
            "so_luong_test = int(input())\n"
            "for _ in range(so_luong_test):\n"
            "    so_can_kiem = int(input())\n"
            "    if kiem_tra_nguyen_to(so_can_kiem):\n"
            "        print('YES')\n"
            "    else:\n"
            "        print('NO')\n"
        )
    elif neu_uoc:
        return (
            "import sys\n"
            "import math\n"
            "input = sys.stdin.readline\n\n"
            "so_luong = int(input())\n"
            "danh_sach_so = list(map(int, input().split()))\n\n"
            "# Tim GCD cua toan bo mang\n"
            "uoc_chung_lon_nhat = danh_sach_so[0]\n"
            "for so_hien_tai in danh_sach_so[1:]:\n"
            "    uoc_chung_lon_nhat = math.gcd(uoc_chung_lon_nhat, so_hien_tai)\n\n"
            "print(uoc_chung_lon_nhat)\n"
        )
    elif neu_sap_xep:
        return (
            "import sys\n"
            "input = sys.stdin.readline\n\n"
            "so_luong_phan_tu = int(input())\n"
            "danh_sach_gia_tri = list(map(int, input().split()))\n\n"
            "# Sap xep tang dan (dung reverse=True neu muon giam dan)\n"
            "danh_sach_da_sap_xep = sorted(danh_sach_gia_tri)\n\n"
            "print(*danh_sach_da_sap_xep)\n"
        )
    elif neu_tinh_tong:
        return (
            "import sys\n"
            "input = sys.stdin.readline\n\n"
            "so_luong_phan_tu = int(input())\n"
            "danh_sach_gia_tri = list(map(int, input().split()))\n\n"
            "# Tinh tong bang ham built-in (nhanh nhat)\n"
            "tong_gia_tri = sum(danh_sach_gia_tri)\n\n"
            "print(tong_gia_tri)\n"
        )
    elif neu_tim_max or neu_tim_min:
        ham = "max" if neu_tim_max else "min"
        return (
            "import sys\n"
            "input = sys.stdin.readline\n\n"
            "so_luong_phan_tu = int(input())\n"
            "danh_sach_gia_tri = list(map(int, input().split()))\n\n"
            f"# Tim gia tri {'lon nhat' if neu_tim_max else 'nho nhat'}\n"
            f"gia_tri_can_tim = {ham}(danh_sach_gia_tri)\n"
            "# Neu can vi tri: vi_tri = danh_sach_gia_tri.index(gia_tri_can_tim)\n\n"
            "print(gia_tri_can_tim)\n"
        )
    elif neu_dem:
        return (
            "import sys\n"
            "from collections import Counter\n"
            "input = sys.stdin.readline\n\n"
            "so_luong_phan_tu = int(input())\n"
            "danh_sach_phan_tu = list(map(int, input().split()))\n\n"
            "# Dem tan suat xuat hien tung phan tu\n"
            "tan_suat_xuat_hien = Counter(danh_sach_phan_tu)\n\n"
            "# Vi du: tim phan tu xuat hien nhieu nhat\n"
            "phan_tu_pho_bien, so_lan = tan_suat_xuat_hien.most_common(1)[0]\n"
            "print(phan_tu_pho_bien, so_lan)\n"
        )
    else:
        return (
            "import sys\n"
            "input = sys.stdin.readline\n\n"
            "# === DOC DU LIEU DAU VAO ===\n"
            "so_luong = int(input())\n"
            "danh_sach_gia_tri = list(map(int, input().split()))\n\n"
            "# === XU LY CHINH ===\n"
            "ket_qua = []  # Danh sach luu ket qua\n\n"
            "for chi_so in range(so_luong):\n"
            "    gia_tri_hien_tai = danh_sach_gia_tri[chi_so]\n"
            "    # TODO: Them logic xu ly tai day theo yeu cau de bai\n"
            "    ket_qua.append(gia_tri_hien_tai)\n\n"
            "# === IN KET QUA ===\n"
            "# In tat ca mot lan (nhanh hon print nhieu lan trong vong lap)\n"
            "print('\\n'.join(map(str, ket_qua)))\n"
        )

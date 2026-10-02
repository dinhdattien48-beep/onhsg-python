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


def analyze_student_code(api_key: str = "", model_name: str = "",
                          problem_desc: str = "", student_code: str = "",
                          judge_results: dict = None) -> str:
    """
    Nhan xet bai lam hoc sinh dua vao de bai + code + ket qua cham.
    - Thu Google Gemini truoc.
    - Neu Gemini loi -> dung Heuristic Engine phan tich code that.
    - Neu diem < 50% -> them phan Code Mau bien tieng Viet.
    """
    api_key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    req_model = (model_name or "").strip() or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()

    diem_dat = (judge_results or {}).get("score", 0)
    tong_test = (judge_results or {}).get("total", 10)
    ty_le_dung = diem_dat / tong_test if tong_test > 0 else 0

    # Yeu cau them code mau khi diem < 50%
    yeu_cau_code_mau = ""
    if ty_le_dung < 0.5:
        yeu_cau_code_mau = """
5. **Code Mau Goi Y** (vi bai dat duoi 50%): Viet 1 doan code Python hoan chinh giai bai tren,
   su dung **ten bien tieng Viet khong dau** (vi du: so_luong, tong_gia_tri, danh_sach_phan_tu, so_nguyen_to)
   de hoc sinh de hieu y nghia tung bien. Them comment tieng Viet giai thich tung buoc quan trong.
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

Hay doc KY code hoc sinh va de bai o tren, sau do nhan xet theo dung {4 + (1 if ty_le_dung < 0.5 else 0)} muc (ngon ngu de hieu, khich le, khong han lam).
Hay viet nhan xet bang tieng Viet co dau, chi doc CODE THAT cua hoc sinh de nhan xet - khong doan mo:

1. **Loi can sua** - Doc code that cua hoc sinh, chi ro:
   - Dong code nao sai / thieu logic gi so voi yeu cau de bai.
   - Truong hop bien nao bi bo sot (so am, so 0, list rong, gia tri cuc lon...).
   - Neu co test WA/TLE/RE, giai thich nguyen nhan cu the trong code.
   - Neu dung het 10/10, khen ngoi cu the diem hay trong code.

2. **Loai bo chi tiet thua** - Chi ra bien du, vong lap khong can thiet hoac doan code vong vo dua vao code hoc sinh.

3. **Toi uu bang ham Built-in Python** - Goi y ham C-level co the thay the doan code thu cong trong bai (sum, max, sorted, Counter, math.gcd...), giai thich ro chuc nang.

4. **Phan tich do phuc tap** - Neu O(...) hien tai cua code hoc sinh, giai thich vi sao nhanh/cham, so sanh voi cach toi uu.
{yeu_cau_code_mau}
Tra loi bang tieng Viet co dau, dung Markdown formatting."""

    # Neu co API Key -> thu Gemini
    if api_key:
        models_to_try = _get_clean_models(req_model)
        for target_model in models_to_try:
            try:
                ket_qua = _call_with_sdk(api_key, target_model, prompt)
                if ket_qua and len(ket_qua.strip()) > 50:
                    return ket_qua
            except Exception:
                pass
            try:
                ket_qua = _call_with_rest(api_key, target_model, prompt)
                if ket_qua and len(ket_qua.strip()) > 50:
                    return ket_qua
            except Exception:
                pass

    # Fallback: Heuristic Engine doc code that
    return generate_heuristic_feedback(problem_desc, student_code, judge_results or {})


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

def generate_heuristic_feedback(problem_desc: str, student_code: str, judge_results: dict) -> str:
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
            "Chuc mung em! Code vuot qua hoan hao 10/10 test cases.\n"
            + _nhan_xet_code_tot(student_code)
        )
    else:
        muc_1 = f"Bai lam dat {diem_dat}/{tong_test} test. Phan tich loi:\n"
        muc_1 += _nhan_xet_loi_cu_the(student_code, problem_desc, ly_do_sai)

    # 2. Chi tiet thua
    muc_2_items = _phat_hien_chi_tiet_thua(student_code)
    muc_2 = "\n".join(f"- {item}" for item in muc_2_items) if muc_2_items else \
        "- Cach khai bao bien ro rang, mach lac, khong co thao tac thua thai."

    # 3. Built-in
    muc_3_items = _goi_y_builtin(student_code, problem_desc)
    muc_3 = "\n".join(f"- {item}" for item in muc_3_items)

    # 4. Do phuc tap
    muc_4 = _phan_tich_do_phuc_tap(student_code)

    # 5. Code mau neu < 50%
    ty_le = diem_dat / tong_test if tong_test > 0 else 1
    muc_5 = ""
    if ty_le < 0.5:
        code_mau = _sinh_code_mau(problem_desc, student_code)
        muc_5 = f"""
#### 5. Code Mau Goi Y (Diem duoi 50% - Xem de hieu huong giai)

> **Day la goi y tham khao** - Em hay doc hieu roi tu viet lai theo cach rieng cua minh!

```python
{code_mau}
```
"""

    return f"""### AI Mentor - Nhan xet bai lam

#### 1. Loi can sua
{muc_1}

#### 2. Loai bo chi tiet thua & Viet code chuan
{muc_2}

#### 3. Toi uu bang ham co san (Built-in) cua Python
{muc_3}

#### 4. Phan tich do phuc tap thuat toan
{muc_4}
{muc_5}"""


def _nhan_xet_code_tot(student_code: str) -> str:
    diem_tot = []
    if "sys.stdin" in student_code:
        diem_tot.append("Em da dung `sys.stdin.readline` - tang toc nhap du lieu chuan HSG.")
    if "def " in student_code:
        diem_tot.append("Em da tach code thanh ham (`def`) - rat chuyen nghiep va de debug.")
    if "sum(" in student_code or "max(" in student_code or "min(" in student_code:
        diem_tot.append("Em da dung ham built-in cua Python (`sum/max/min`) - thuc hanh chuan thi HSG.")
    if not diem_tot:
        diem_tot.append("Code chinh xac, xu ly dung yeu cau de bai.")
    return "\n".join(f"- {d}" for d in diem_tot)


def _nhan_xet_loi_cu_the(student_code: str, problem_desc: str, ly_do_sai: set) -> str:
    cac_loi = []

    if "TLE" in ly_do_sai:
        so_vong_lap = student_code.count("for ") + student_code.count("while ")
        if so_vong_lap >= 2:
            cac_loi.append(
                f"**Qua gioi han thoi gian (TLE):** Em dang dung nhieu vong lap long nhau "
                f"(phat hien {so_vong_lap} vong lap trong code). "
                "Voi du lieu lon, O(N^2) se vuot qua 1 giay. "
                "Hay thu dung `sum()`, `Counter`, hoac sap xep mot lan roi dung hai con tro."
            )
        else:
            cac_loi.append(
                "**Qua gioi han thoi gian (TLE):** Phep tinh trong vong lap dang qua nang. "
                "Them `import sys; input = sys.stdin.readline` va kiem tra co the "
                "dung ham built-in thay the khong."
            )

    if "WA" in ly_do_sai:
        thieu_bien = []
        if student_code.count("if ") < 2:
            thieu_bien.append("kiem tra dieu kien bien")
        mo_ta_bien = f" (co the thieu xu ly: {', '.join(thieu_bien)})" if thieu_bien else ""
        cac_loi.append(
            f"**Ket qua sai (WA){mo_ta_bien}:** Thuat toan bi sai o mot so truong hop. "
            "Hay test thu: n=0, n=1, tat ca phan tu bang nhau, gia tri toi da 10^9."
        )

    if "RE" in ly_do_sai:
        nguyen_nhan = []
        if "/" in student_code:
            nguyen_nhan.append("`ZeroDivisionError` - chia co the bi chia cho 0")
        if "[" in student_code and "]" in student_code:
            nguyen_nhan.append("`IndexError` - truy cap phan tu ngoai gioi han mang")
        mo_ta = "; ".join(nguyen_nhan) if nguyen_nhan else "chia cho 0 hoac truy cap mang ngoai bien"
        cac_loi.append(
            f"**Loi thuc thi (RE):** Nguyen nhan co the trong code: {mo_ta}. "
            "Them dieu kien kiem tra truoc khi tinh toan."
        )

    if not cac_loi:
        cac_loi.append("Chua xac dinh duoc loi cu the - hay thu chay thu tung test nho.")

    return "\n".join(f"- {loi}" for loi in cac_loi)


def _phat_hien_chi_tiet_thua(student_code: str) -> list:
    items = []

    if "while " in student_code and "for " not in student_code:
        items.append(
            "Neu da biet truoc so vong lap, dung `for i in range(n)` thay `while` "
            "de code ngan hon va tranh lap vo tan."
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
            f"Em dang goi `print()` ~{print_trong_vong_lap} lan trong vong lap. "
            "Hay gom ket qua vao list roi dung `print('\\n'.join(ket_qua))` de in mot lan - nhanh hon nhieu."
        )

    if " = list()" in student_code:
        items.append("Dung `[]` thay `list()` de khoi tao list - ngan hon va chuan Pythonic.")

    return items


def _goi_y_builtin(student_code: str, problem_desc: str) -> list:
    items = []
    de_lower = problem_desc.lower()

    if "+=" in student_code and ("for " in student_code or "while " in student_code) and "sum(" not in student_code:
        items.append(
            "**`sum(iterable)`**: Em dang cong don thu cong trong vong lap. "
            "Ham `sum()` viet bang C, nhanh 3-5 lan: `tong = sum(danh_sach)`"
        )

    if (">" in student_code or "<" in student_code) and "max(" not in student_code and "min(" not in student_code:
        if re.search(r'if .+[><].+:', student_code):
            items.append(
                "**`max()` / `min()`**: Thay vi so sanh thu cong bang `if`, "
                "dung `max(a, b)` hoac `max(danh_sach)` - ngan gon hon rat nhieu."
            )

    if ("uoc" in de_lower or "gcd" in student_code.lower() or "boi" in de_lower) and "math.gcd" not in student_code:
        items.append(
            "**`math.gcd(a, b)`**: Tim uoc chung lon nhat sieu nhanh: "
            "`import math; ket_qua = math.gcd(so_a, so_b)`."
        )

    if re.search(r'\w+\[.+\]\s*\+=\s*1', student_code) and "Counter" not in student_code:
        items.append(
            "**`Counter(iterable)`** tu `collections`: Dem tan suat phan tu cuc nhanh: "
            "`from collections import Counter; tan_suat = Counter(danh_sach)`."
        )

    if "sys.stdin" not in student_code:
        items.append(
            "**Tang toc nhap lieu**: Them 2 dong dau bai: `import sys` va `input = sys.stdin.readline` "
            "- tang toc doc du lieu 5-10 lan khi co nhieu dong nhap."
        )

    if not items:
        items.append(
            "Em da dung kha tot cac cau truc chuan Python. "
            "Tiep tuc thuc hanh `list comprehension` va cac ham built-in nhe!"
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
            f"- **Do phuc tap hien tai:** Khoang **O(N^3)** (co {do_sau_max} vong lap long nhau).\n"
            "- Nguy hiem! Voi N >= 1000, se bi TLE ngay. Can tai cau truc thuat toan."
        )
    elif do_sau_max == 2:
        return (
            "- **Do phuc tap hien tai:** Khoang **O(N^2)** (2 vong lap long nhau).\n"
            "- Chap nhan duoc voi N <= 5000, nhung se TLE khi N >= 100000. "
            "Hay thu dung hai con tro hoac Hashing de dat O(N)."
        )
    elif do_sau_max == 1 and co_sort:
        return (
            "- **Do phuc tap hien tai:** Khoang **O(N log N)** (1 vong lap + sap xep).\n"
            "- Rat tot! Du nhanh voi N <= 1000000."
        )
    elif do_sau_max == 1:
        return (
            "- **Do phuc tap hien tai:** Khoang **O(N)** (chi 1 vong lap don).\n"
            "- Xuat sac! Xu ly duoc N = 10^7 trong 1 giay."
        )
    else:
        return (
            "- **Do phuc tap hien tai:** **O(1)** hoac O(log N).\n"
            "- Toi uu tuyet doi!"
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

"""
seed_data.py - Dữ liệu giáo trình đầy đủ cho 8 chặng luyện thi HSG Tin học Python.
Lý thuyết viết bằng tiếng Việt, biến đặt tên tiếng Việt để dễ hiểu.
Bao gồm: Lý thuyết chi tiết, Góc Vũ Khí Python, 3 bài tập mỗi chặng,
generator tạo 10 test cases và solution chuẩn cho mỗi bài.
"""

import random
import math
from collections import Counter
from itertools import accumulate

# ============================================================================
# HÀM TIỆN ÍCH TẠO TEST
# ============================================================================

def _make_test(inp: str, out: str) -> dict:
    """Tạo một test case từ input và expected output."""
    return {"input": inp.strip(), "expected_output": out.strip()}


# ============================================================================
# CHẶNG 1: LÀM QUEN PYTHON & NHẬP XUẤT CHUẨN THI HSG
# ============================================================================

STAGE_1_THEORY = r"""
# 🚀 Chặng 1: Làm quen Python & Nhập xuất chuẩn thi HSG

## 1. Python là gì? Tại sao dùng Python để thi HSG?

Python là ngôn ngữ lập trình **rất thân thiện với người mới bắt đầu**. Thay vì phải viết hàng chục dòng như C++, Python cho phép em giải bài chỉ trong vài dòng ngắn gọn.

> **Lợi thế lớn nhất của Python trong thi HSG:** Số nguyên trong Python **KHÔNG BỊ TRÀN SỐ** — em có thể tính $10^{1000}$ thoải mái mà không cần lo lắng!

## 2. Biến — "Chiếc hộp" lưu dữ liệu

**Biến** giống như một chiếc hộp có nhãn dán, dùng để lưu giá trị. Python tự nhận biết kiểu dữ liệu, em không cần khai báo trước.

```python
# Số nguyên — dùng nhiều nhất trong thi HSG
tuoi = 16
so_hoc_sinh = 35
diem_thi = -5        # Số nguyên có thể âm

# Số thực — ít dùng, cẩn thận sai số khi so sánh
chieu_cao = 1.75

# Chuỗi ký tự (văn bản)
ten_truong = "THPT Chu Văn An"

# Boolean — chỉ có True (đúng) hoặc False (sai)
da_hoc_xong = False

# In ra màn hình để kiểm tra
print(tuoi)           # Kết quả: 16
print(ten_truong)     # Kết quả: THPT Chu Văn An
```

### Quy tắc đặt tên biến:
- ✅ Dùng chữ thường, nối bằng dấu gạch dưới: `so_nguyen_to`, `ket_qua`
- ✅ Có thể có số ở cuối: `so1`, `mang_a2`
- ❌ Không bắt đầu bằng số: `1bien` (SAI)
- ❌ Không có dấu cách: `so nguyen` (SAI)

## 3. Hàm `print()` — In kết quả ra màn hình

```python
diem_a = 9
diem_b = 8

# In một giá trị
print(diem_a)              # Kết quả: 9

# In nhiều giá trị cùng lúc (cách nhau bằng dấu cách)
print(diem_a, diem_b)      # Kết quả: 9 8

# Tuỳ chỉnh ký tự phân cách bằng sep=
print(diem_a, diem_b, sep=", ")   # Kết quả: 9, 8

# Không xuống dòng sau khi in bằng end=
print("Xin chào", end=" ")
print("Python!")           # Kết quả: Xin chào Python!
```

## 4. Hàm `input()` — Đọc dữ liệu nhập vào

Trong thi HSG, máy chấm bài tự động nhập dữ liệu vào chương trình của em. `input()` đọc **một dòng** và luôn trả về **chuỗi ký tự** (string).

```python
# Đọc một chuỗi
ten = input()          # Người dùng nhập: "Minh" → ten = "Minh"

# Đọc một số nguyên — PHẢI chuyển kiểu bằng int()
so_thu_nhat = int(input())    # Nhập: 42 → so_thu_nhat = 42

# Nếu quên int() thì sao?
gia_tri = input()      # Nhập: 5
print(gia_tri + 3)     # LỖI! Không thể cộng chuỗi với số
```

## 5. Đọc nhiều số trên cùng một dòng — Kỹ thuật QUAN TRỌNG NHẤT

Trong đề thi HSG, dữ liệu thường cho dạng:
```
3 5
```
Nghĩa là hai số `chieu_dai = 3` và `chieu_rong = 5` trên cùng một dòng.

```python
# ✅ CÁCH CHUẨN — dùng map() + split()
chieu_dai, chieu_rong = map(int, input().split())

# Giải thích từng bước:
# Bước 1: input()          → đọc cả dòng: "3 5"
# Bước 2: .split()         → tách thành list: ["3", "5"]
# Bước 3: map(int, ...)    → chuyển từng phần tử thành số: [3, 5]
# Bước 4: chieu_dai, chieu_rong = ... → gán vào biến: 3 và 5

# Đọc nhiều số vào một danh sách (mảng)
so_luong = int(input())
danh_sach_so = list(map(int, input().split()))
```

### Ví dụ đầy đủ — Tính chu vi hình chữ nhật:

```python
# Đọc chiều dài và chiều rộng trên 1 dòng
chieu_dai, chieu_rong = map(int, input().split())

# Tính chu vi
chu_vi = 2 * (chieu_dai + chieu_rong)

# In kết quả
print(chu_vi)
```

## 6. Tăng tốc đọc dữ liệu lớn với `sys.stdin.readline`

Khi đề bài có $N \le 10^5$ hoặc $10^6$ dòng dữ liệu, `input()` thông thường **rất chậm**. Dùng thủ thuật này để nhanh hơn 3-5 lần:

```python
import sys
input = sys.stdin.readline   # Ghi đè hàm input gốc bằng readline

# Từ đây, mọi lệnh input() đều dùng readline — nhanh hơn nhiều!
so_luong = int(input())
danh_sach = list(map(int, input().split()))
```

> ⚠️ `sys.stdin.readline` giữ ký tự `\n` ở cuối, nhưng `int()` và `split()` tự bỏ qua nên không ảnh hưởng.
"""

STAGE_1_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `map()` và `sys.stdin.readline`

### Vũ khí 1: `map(hàm, danh_sách)`

| Thuộc tính | Chi tiết |
|---|---|
| **Tên hàm** | `map()` |
| **Cú pháp** | `map(int, input().split())` |
| **Cách hoạt động** | Áp dụng hàm `int` lên **từng phần tử** trong danh sách, chạy ở tầng C nhanh hơn vòng lặp Python |
| **Độ phức tạp** | $O(N)$ — nhưng hằng số nhỏ hơn vòng lặp thông thường |

```python
# ❌ Cách chậm — tự viết vòng lặp
cac_phan_tu = input().split()       # ["3", "5", "7"]
danh_sach_so = []
for phan_tu in cac_phan_tu:
    danh_sach_so.append(int(phan_tu))

# ✅ Cách nhanh — dùng map (chạy ở tầng C)
danh_sach_so = list(map(int, input().split()))
# Chỉ 1 dòng, nhanh hơn 2-3 lần!
```

### Vũ khí 2: `sys.stdin.readline`

| Thuộc tính | Chi tiết |
|---|---|
| **Tên** | `sys.stdin.readline` |
| **Cú pháp** | `import sys` rồi `input = sys.stdin.readline` |
| **Tốc độ** | Nhanh hơn `input()` gốc **3-5 lần** khi đọc $\ge 10^5$ dòng |
| **Cách dùng** | Thêm 2 dòng đầu chương trình, phần còn lại dùng `input()` bình thường |
"""

# ---------- Bài tập Chặng 1 ----------

def _gen_tests_1_1():
    """Bài 1.1: Tổng hai số nguyên."""
    tests = []
    tests.append(_make_test("3 5", "8"))
    tests.append(_make_test("0 0", "0"))
    tests.append(_make_test("100 200", "300"))
    tests.append(_make_test("-5 5", "0"))
    tests.append(_make_test("-100 -200", "-300"))
    tests.append(_make_test("1000000 999999", "1999999"))
    tests.append(_make_test("999999999 1", "1000000000"))
    tests.append(_make_test("123456789 987654321", "1111111110"))
    tests.append(_make_test("-999999999 999999999", "0"))
    tests.append(_make_test("1000000000 1000000000", "2000000000"))
    return tests

def _gen_tests_1_2():
    """Bài 1.2: Chu vi và Diện tích hình chữ nhật."""
    tests = []
    tests.append(_make_test("3 5", "15\n16"))
    tests.append(_make_test("1 1", "1\n4"))
    tests.append(_make_test("10 20", "200\n60"))
    tests.append(_make_test("0 5", "0\n10"))
    tests.append(_make_test("1 1000000", "1000000\n2000002"))
    tests.append(_make_test("999 1001", "999999\n4000"))
    tests.append(_make_test("100000 100000", "10000000000\n400000"))
    random.seed(42)
    for _ in range(3):
        a = random.randint(1, 10**6)
        b = random.randint(1, 10**6)
        s = a * b
        p = 2 * (a + b)
        tests.append(_make_test(f"{a} {b}", f"{s}\n{p}"))
    return tests

def _gen_tests_1_3():
    """Bài 1.3: Tổng N số. Stress test N=10^6."""
    tests = []
    tests.append(_make_test("3\n1 2 3", "6"))
    tests.append(_make_test("1\n42", "42"))
    tests.append(_make_test("5\n10 20 30 40 50", "150"))
    tests.append(_make_test("4\n-1 -2 -3 -4", "-10"))
    tests.append(_make_test("3\n0 0 0", "0"))
    tests.append(_make_test("2\n1000000000 1000000000", "2000000000"))
    tests.append(_make_test("5\n-1000000 1000000 -1000000 1000000 0", "0"))
    random.seed(101)
    for so_luong in [100000, 500000, 1000000]:
        cac_so = [random.randint(-10**6, 10**6) for _ in range(so_luong)]
        tong = sum(cac_so)
        du_lieu_vao = f"{so_luong}\n{' '.join(map(str, cac_so))}"
        tests.append(_make_test(du_lieu_vao, str(tong)))
    return tests


STAGE_1_PROBLEMS = [
    {
        "id": "1_1",
        "stage_id": 1,
        "order": 1,
        "title": "Tổng hai số",
        "difficulty": "Khởi động",
        "time_limit": 1.0,
        "description": r"""## Tổng hai số

### Đề bài
Cho hai số nguyên $a$ và $b$. Hãy tính và in ra tổng $a + b$.

### Input
- Một dòng duy nhất chứa hai số nguyên $a$ và $b$ cách nhau bởi dấu cách ($-10^9 \le a, b \le 10^9$).

### Output
- In ra một số nguyên duy nhất là tổng $a + b$.

### Ví dụ
| Input | Output |
|-------|--------|
| `3 5` | `8` |
| `0 0` | `0` |
| `-5 5` | `0` |

### Gợi ý
Đây là bài tập đầu tiên! Em chỉ cần dùng `map(int, input().split())` để đọc hai số, rồi `print()` để in kết quả.
""",
    },
    {
        "id": "1_2",
        "stage_id": 1,
        "order": 2,
        "title": "Chu vi và Diện tích",
        "difficulty": "Vận dụng",
        "time_limit": 1.0,
        "description": r"""## Chu vi và Diện tích hình chữ nhật

### Đề bài
Cho hình chữ nhật có chiều dài $a$ và chiều rộng $b$. Hãy tính diện tích $S = a \times b$ và chu vi $P = 2 \times (a + b)$.

### Input
- Một dòng chứa hai số nguyên không âm $a$ và $b$ ($0 \le a, b \le 10^6$).

### Output
- Dòng 1: In diện tích $S$.
- Dòng 2: In chu vi $P$.

### Ví dụ
| Input | Output |
|-------|--------|
| `3 5` | `15`<br>`16` |
| `1 1` | `1`<br>`4` |

### Gợi ý
Bài này luyện cách in kết quả trên nhiều dòng bằng hai lệnh `print()`.
""",
    },
    {
        "id": "1_3",
        "stage_id": 1,
        "order": 3,
        "title": "Tổng N số",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 1.0,
        "description": r"""## Tổng N số

### Đề bài
Cho $N$ số nguyên. Hãy tính tổng của chúng.

### Input
- Dòng 1: Số nguyên dương $N$ ($1 \le N \le 10^6$).
- Dòng 2: $N$ số nguyên $a_1, a_2, \ldots, a_N$ cách nhau bởi dấu cách ($|a_i| \le 10^6$).

### Output
- In ra tổng $a_1 + a_2 + \ldots + a_N$.

### Ví dụ
| Input | Output |
|-------|--------|
| `3`<br>`1 2 3` | `6` |
| `5`<br>`10 20 30 40 50` | `150` |

### Gợi ý
⚠️ Với $N$ lên đến $10^6$, em cần dùng `sys.stdin.readline` để tăng tốc đọc dữ liệu, và hàm `sum()` (chạy ở tầng C) thay vì vòng lặp Python thủ công.
""",
    },
]


# ============================================================================
# CHẶNG 2: RẼ NHÁNH & TOÁN HỌC THÔNG MINH
# ============================================================================

STAGE_2_THEORY = r"""
# 🔀 Chặng 2: Rẽ nhánh & Toán học thông minh

## 1. Câu lệnh điều kiện `if - elif - else`

Trong cuộc sống, ta luôn phải đưa ra quyết định dựa trên điều kiện. Python dùng `if` để làm điều đó:

```python
diem_thi = int(input())

if diem_thi >= 8:
    print("Giỏi")
elif diem_thi >= 6.5:
    print("Khá")
elif diem_thi >= 5:
    print("Trung bình")
else:
    print("Yếu")
```

### Giải thích cú pháp:
- Sau `if`, `elif`, `else` phải có dấu **hai chấm** `:`
- Code bên trong phải **thụt vào 4 dấu cách** (Tab) — Python rất nghiêm khắc về điều này!
- `elif` = "else if" — kiểm tra tiếp khi điều kiện trước KHÔNG đúng
- `else` — chạy khi TẤT CẢ điều kiện trên đều sai

### Các toán tử so sánh:

| Toán tử | Ý nghĩa | Ví dụ | Kết quả |
|---------|---------|-------|---------|
| `==` | Bằng nhau | `5 == 5` | `True` |
| `!=` | Khác nhau | `5 != 3` | `True` |
| `<` | Nhỏ hơn | `3 < 5` | `True` |
| `>` | Lớn hơn | `5 > 3` | `True` |
| `<=` | Nhỏ hơn hoặc bằng | `5 <= 5` | `True` |
| `>=` | Lớn hơn hoặc bằng | `6 >= 5` | `True` |

### Kết hợp nhiều điều kiện:
```python
tuoi = 16
diem = 8.5

# and — CẢ HAI điều kiện đều phải đúng
if tuoi >= 15 and diem >= 8:
    print("Đủ điều kiện thi học sinh giỏi")

# or — Ít nhất MỘT điều kiện đúng
if diem == 10 or tuoi <= 14:
    print("Xuất sắc hoặc còn trẻ")

# not — Phủ định (đảo ngược)
if not (diem < 5):
    print("Không bị yếu")   # Tức là diem >= 5
```

## 2. Phép chia nguyên `//` và chia lấy dư `%`

Đây là hai phép toán **cực kỳ quan trọng** trong thi HSG:

```python
# Chia nguyên — lấy phần nguyên của thương
17 // 5    # = 3   (17 chia 5 được 3, dư 2)
20 // 4    # = 5   (20 chia 4 được đúng 5)

# Chia lấy dư — lấy phần dư
17 % 5     # = 2   (17 = 5 × 3 + 2)
20 % 4     # = 0   (20 chia hết cho 4)
10 % 3     # = 1   (10 = 3 × 3 + 1)
```

### Ứng dụng thực tế:
```python
so_can_kiem_tra = int(input())

# Kiểm tra số chẵn hay lẻ
if so_can_kiem_tra % 2 == 0:
    print("Chẵn")
else:
    print("Lẻ")

# Lấy chữ số hàng đơn vị của một số
so = 2024
hang_don_vi = so % 10          # 4
hang_chuc = (so // 10) % 10    # 2
hang_tram = (so // 100) % 10   # 0
```

## 3. Các hàm toán học cơ bản

```python
gia_tri_a = -7
gia_tri_b = 3

# abs() — Giá trị tuyệt đối (bỏ dấu âm)
print(abs(gia_tri_a))         # 7
print(abs(gia_tri_b))         # 3

# min() — Tìm giá trị nhỏ nhất
so_nho_hon = min(gia_tri_a, gia_tri_b)    # -7

# max() — Tìm giá trị lớn nhất
so_lon_hon = max(gia_tri_a, gia_tri_b)    # 3

# Có thể truyền nhiều số một lúc
ket_qua_min = min(3, 1, 4, 1, 5, 9, 2)   # 1
ket_qua_max = max(3, 1, 4, 1, 5, 9, 2)   # 9
```

## 4. Lũy thừa và chia dư — Bẫy phổ biến trong thi HSG

```python
co_so = 2
so_mu = 10
chia_du_cho = 1000

# Tính 2^10 = 1024
ket_qua = co_so ** so_mu    # 1024

# Tính 2^10 mod 1000 (SAI — tốn bộ nhớ với số mu lớn)
ket_qua_sai = (co_so ** so_mu) % chia_du_cho

# Tính 2^10 mod 1000 (ĐÚNG — dùng pow 3 tham số)
ket_qua_dung = pow(co_so, so_mu, chia_du_cho)    # Nhanh hơn nhiều!
```
"""

STAGE_2_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `min()`, `max()`, `abs()` và `pow(a, b, mod)`

### Vũ khí 1: `min()` và `max()`

| Thuộc tính | Chi tiết |
|---|---|
| **Tên hàm** | `min()` / `max()` |
| **Cú pháp** | `min(so_a, so_b)` hoặc `min(danh_sach)` |
| **Cách hoạt động** | Tìm giá trị nhỏ nhất / lớn nhất. Chạy ở tầng C — nhanh hơn tự viết `if`. |
| **Độ phức tạp** | $O(N)$ với N phần tử, hằng số nhỏ |

### Vũ khí 2: `pow(co_so, so_mu, chia_du)` — Lũy thừa nhanh có chia dư

| Thuộc tính | Chi tiết |
|---|---|
| **Tên hàm** | `pow(a, b, mod)` |
| **Cú pháp** | `pow(2, 100, 1000000007)` |
| **Cách hoạt động** | Tính $a^b \mod m$ bằng **bình phương và nhân** (binary exponentiation) ở tầng C |
| **Độ phức tạp** | $O(\log b)$ — cực nhanh dù $b = 10^{18}$ |

```python
co_so = 2
so_mu = 1000000000000000000   # b = 10^18
mo_dun = 1000000007

# ❌ SAI — tính 2^(10^18) thành số khổng lồ, máy đứng luôn!
ket_qua_sai = (co_so ** so_mu) % mo_dun

# ❌ Chậm — vòng lặp nhân 10^18 lần, mất hàng triệu năm!
ket_qua_cham = 1
for buoc in range(so_mu):
    ket_qua_cham = (ket_qua_cham * co_so) % mo_dun

# ✅ ĐÚNG và NHANH — pow 3 tham số, chạy trong 0.0001 giây!
ket_qua_dung = pow(co_so, so_mu, mo_dun)
```
"""

def _gen_tests_2_1():
    tests = []
    tests.append(_make_test("4", "CHAN"))
    tests.append(_make_test("7", "LE"))
    tests.append(_make_test("0", "CHAN"))
    tests.append(_make_test("-3", "LE"))
    tests.append(_make_test("-4", "CHAN"))
    tests.append(_make_test("1", "LE"))
    tests.append(_make_test("1000000000", "CHAN"))
    tests.append(_make_test("999999999", "LE"))
    tests.append(_make_test("-999999998", "CHAN"))
    tests.append(_make_test("2", "CHAN"))
    return tests

def _gen_tests_2_2():
    tests = []
    tests.append(_make_test("3 5 1", "5"))
    tests.append(_make_test("10 10 10", "10"))
    tests.append(_make_test("-1 -2 -3", "-1"))
    tests.append(_make_test("0 0 0", "0"))
    tests.append(_make_test("-5 0 5", "5"))
    tests.append(_make_test("1000000000 999999999 999999998", "1000000000"))
    tests.append(_make_test("-1000000000 -999999999 -999999998", "-999999998"))
    random.seed(202)
    for _ in range(3):
        a, b, c = [random.randint(-10**9, 10**9) for _ in range(3)]
        tests.append(_make_test(f"{a} {b} {c}", str(max(a, b, c))))
    return tests

def _gen_tests_2_3():
    tests = []
    tests.append(_make_test("2 10 1000", "24"))
    tests.append(_make_test("3 3 100", "27"))
    tests.append(_make_test("2 0 100", "1"))
    tests.append(_make_test("0 5 100", "0"))
    tests.append(_make_test("5 1 3", "2"))
    tests.append(_make_test("2 31 1000000007", str(pow(2, 31, 1000000007))))
    tests.append(_make_test("123 456 1000000007", str(pow(123, 456, 1000000007))))
    tests.append(_make_test("999999999 1000000000000000000 1000000007",
                            str(pow(999999999, 10**18, 1000000007))))
    tests.append(_make_test("2 1000000000000000000 998244353",
                            str(pow(2, 10**18, 998244353))))
    tests.append(_make_test("123456789 999999999999999999 1000000007",
                            str(pow(123456789, 999999999999999999, 1000000007))))
    return tests


STAGE_2_PROBLEMS = [
    {
        "id": "2_1",
        "stage_id": 2,
        "order": 1,
        "title": "Chẵn hay Lẻ?",
        "difficulty": "Khởi động",
        "time_limit": 1.0,
        "description": r"""## Chẵn hay Lẻ?

### Đề bài
Cho một số nguyên $N$. Hãy kiểm tra $N$ là số chẵn hay số lẻ.

### Input
- Một dòng chứa số nguyên $N$ ($-10^9 \le N \le 10^9$).

### Output
- In `CHAN` nếu $N$ chẵn, `LE` nếu $N$ lẻ.

### Ví dụ
| Input | Output |
|-------|--------|
| `4` | `CHAN` |
| `7` | `LE` |
| `0` | `CHAN` |

### Gợi ý
Dùng phép chia lấy dư `%` để kiểm tra. Lưu ý: số 0 là số chẵn!
""",
    },
    {
        "id": "2_2",
        "stage_id": 2,
        "order": 2,
        "title": "Max trong 3 số",
        "difficulty": "Vận dụng",
        "time_limit": 1.0,
        "description": r"""## Tìm số lớn nhất trong 3 số

### Đề bài
Cho ba số nguyên $a$, $b$, $c$. Hãy tìm giá trị lớn nhất.

### Input
- Một dòng chứa ba số nguyên $a, b, c$ ($-10^9 \le a, b, c \le 10^9$).

### Output
- In ra giá trị lớn nhất trong ba số.

### Ví dụ
| Input | Output |
|-------|--------|
| `3 5 1` | `5` |
| `10 10 10` | `10` |
| `-1 -2 -3` | `-1` |

### Gợi ý
Em có thể dùng nhiều lệnh `if`, nhưng cách tối ưu là dùng hàm `max()` — chỉ cần 1 dòng code!
""",
    },
    {
        "id": "2_3",
        "stage_id": 2,
        "order": 3,
        "title": "Lũy thừa nhanh",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 1.0,
        "description": r"""## Lũy thừa có chia dư

### Đề bài
Cho ba số nguyên $a$, $b$, $m$. Hãy tính $a^b \mod m$.

### Input
- Một dòng chứa ba số nguyên $a$, $b$, $m$ ($0 \le a \le 10^9$, $0 \le b \le 10^{18}$, $1 \le m \le 10^9 + 7$).

### Output
- In ra $a^b \mod m$.

### Ví dụ
| Input | Output |
|-------|--------|
| `2 10 1000` | `24` |
| `3 3 100` | `27` |

### ⚠️ Cảnh báo
$b$ có thể lên tới $10^{18}$! Nếu em dùng vòng lặp nhân lặp $O(b)$ lần, chương trình sẽ **chạy mãi không xong**. Hãy nhớ Vũ Khí Python: `pow(a, b, m)` chạy trong $O(\log b)$!
""",
    },
]

# ============================================================================
# CHẶNG 3: VÒNG LẶP & TƯ DUY KHỬ VÒNG LẶP
# ============================================================================

STAGE_3_THEORY = r"""
# 🔄 Chặng 3: Vòng lặp & Tư duy khử vòng lặp

## 1. Vòng lặp `for` — Lặp đi lặp lại một số lần xác định

Khi cần làm đi làm lại một việc nhiều lần, ta dùng vòng lặp `for`:

```python
# In các số từ 1 đến 5
for so_thu_tu in range(1, 6):    # range(1, 6) = dãy 1, 2, 3, 4, 5
    print(so_thu_tu)

# Tính tổng từ 1 đến 10
tong = 0
for so_hien_tai in range(1, 11):
    tong = tong + so_hien_tai    # Hoặc viết gọn: tong += so_hien_tai
print(tong)    # 55
```

### Hàm `range()` — Tạo dãy số:

```python
range(5)           # 0, 1, 2, 3, 4         (bắt đầu từ 0)
range(1, 6)        # 1, 2, 3, 4, 5         (không bao gồm 6)
range(0, 10, 2)    # 0, 2, 4, 6, 8         (bước nhảy 2)
range(10, 0, -1)   # 10, 9, 8, ..., 1      (đếm ngược)
range(5, -1, -1)   # 5, 4, 3, 2, 1, 0      (từ 5 xuống 0)
```

### Ví dụ thực tế:
```python
so_hoc_sinh = int(input())
tong_diem = 0

for thu_tu in range(so_hoc_sinh):    # Lặp so_hoc_sinh lần
    diem_hoc_sinh = int(input())
    tong_diem += diem_hoc_sinh

diem_trung_binh = tong_diem / so_hoc_sinh
print(diem_trung_binh)
```

## 2. Vòng lặp `while` — Lặp khi điều kiện còn đúng

Dùng khi **không biết trước** sẽ lặp bao nhiêu lần:

```python
# Đếm số chữ số của một số nguyên
so_nguyen = 123456
so_chu_so = 0

while so_nguyen > 0:
    so_nguyen = so_nguyen // 10    # Bỏ chữ số cuối
    so_chu_so += 1

print(so_chu_so)    # 6

# Tìm số nguyên tố đầu tiên lớn hơn 100
so_kiem_tra = 101
while True:
    la_nguyen_to = True
    for uoc in range(2, so_kiem_tra):
        if so_kiem_tra % uoc == 0:
            la_nguyen_to = False
            break
    if la_nguyen_to:
        print(so_kiem_tra)
        break
    so_kiem_tra += 1
```

## 3. Lệnh `break` và `continue`

```python
# break — Thoát khỏi vòng lặp ngay lập tức
for so in range(1, 11):
    if so == 5:
        break          # Dừng khi gặp số 5
    print(so)
# In ra: 1, 2, 3, 4

# continue — Bỏ qua lần lặp hiện tại, sang lần tiếp theo
for so in range(1, 11):
    if so % 2 == 0:
        continue       # Bỏ qua số chẵn
    print(so)
# In ra: 1, 3, 5, 7, 9
```

## 4. Tư duy QUAN TRỌNG: Khi nào phải khử vòng lặp?

Máy tính xử lý khoảng $10^8$ phép tính/giây. Vì vậy:

| Giá trị N | Giải pháp |
|-----------|-----------|
| $N \le 10^6$ | Vòng lặp $O(N)$ vẫn chấp nhận được |
| $N \le 10^8$ | Cần thuật toán $O(\sqrt{N})$ hoặc $O(N\log N)$ |
| $N \ge 10^9$ | **Bắt buộc** phải tìm công thức $O(1)$ hoặc $O(\log N)$ |

### Ví dụ kinh điển — Tính $1 + 2 + 3 + \ldots + N$:

```python
so_hang = int(input())    # N

# ❌ Cách ngây thơ: vòng lặp O(N) — với N = 10^18 sẽ chạy mãi!
tong_vong_lap = 0
for so in range(1, so_hang + 1):
    tong_vong_lap += so

# ✅ Cách thông minh: Công thức Gauss O(1) — chạy tức thì!
# Gauss phát hiện: 1+2+...+N = N×(N+1)/2
tong_cong_thuc = so_hang * (so_hang + 1) // 2

print(tong_cong_thuc)
```

> 💡 **Câu chuyện thú vị:** Năm 10 tuổi, nhà toán học Gauss được thầy giáo ra bài tính $1 + 2 + ... + 100$ để học sinh bận rộn. Gauss tìm ra công thức trong vài giây và là người đầu tiên nộp bài!

### Một số công thức $O(1)$ hay gặp trong thi HSG:

| Bài toán | Công thức | Độ phức tạp |
|----------|-----------|-------------|
| $1 + 2 + \ldots + N$ | $\dfrac{N(N+1)}{2}$ | $O(1)$ |
| $1^2 + 2^2 + \ldots + N^2$ | $\dfrac{N(N+1)(2N+1)}{6}$ | $O(1)$ |
| $1 + 3 + 5 + \ldots + (2N-1)$ | $N^2$ | $O(1)$ |
"""

STAGE_3_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `sum()` và công thức toán $O(1)$

### Vũ khí 1: `sum(danh_sach)`

| Thuộc tính | Chi tiết |
|---|---|
| **Tên hàm** | `sum()` |
| **Cú pháp** | `sum([1, 2, 3])` hoặc `sum(range(1, n+1))` |
| **Cách hoạt động** | Tính tổng tất cả phần tử. Chạy ở tầng C, nhanh hơn vòng `for` Python 2-3 lần |
| **Độ phức tạp** | $O(N)$ — hằng số nhỏ |

```python
danh_sach_so = [3, 1, 4, 1, 5, 9, 2, 6]

# ❌ Cách chậm — tự viết vòng lặp
tong_thu_cong = 0
for phan_tu in danh_sach_so:
    tong_thu_cong += phan_tu

# ✅ Cách nhanh — dùng sum()
tong_nhanh = sum(danh_sach_so)    # Chỉ 1 dòng, chạy ở tầng C!
```

### Vũ khí 2: Tư duy khử vòng lặp bằng công thức toán

```python
N = 10**18    # N = 1 tỷ tỷ

# ❌ Vòng lặp: O(N) — với N = 10^18, cần 10^10 giây ≈ 317 năm!
tong_vong_lap = 0
for so in range(1, N + 1):
    tong_vong_lap += so

# ✅ Công thức Gauss: O(1) — chạy trong 0.000001 giây!
tong_cong_thuc = N * (N + 1) // 2
```
"""

def _gen_tests_3_1():
    tests = []
    tests.append(_make_test("5", "1\n2\n3\n4\n5"))
    tests.append(_make_test("1", "1"))
    tests.append(_make_test("3", "1\n2\n3"))
    tests.append(_make_test("10", "\n".join(str(i) for i in range(1, 11))))
    tests.append(_make_test("2", "1\n2"))
    tests.append(_make_test("20", "\n".join(str(i) for i in range(1, 21))))
    tests.append(_make_test("50", "\n".join(str(i) for i in range(1, 51))))
    tests.append(_make_test("100", "\n".join(str(i) for i in range(1, 101))))
    tests.append(_make_test("500", "\n".join(str(i) for i in range(1, 501))))
    tests.append(_make_test("1000", "\n".join(str(i) for i in range(1, 1001))))
    return tests

def _gen_tests_3_2():
    def count_divisors(n):
        if n == 0: return 0
        n = abs(n)
        count = 0
        i = 1
        while i * i <= n:
            if n % i == 0:
                count += 1
                if i != n // i:
                    count += 1
            i += 1
        return count

    tests = []
    tests.append(_make_test("12", str(count_divisors(12))))
    tests.append(_make_test("1", "1"))
    tests.append(_make_test("7", "2"))
    tests.append(_make_test("100", str(count_divisors(100))))
    tests.append(_make_test("2", "2"))
    tests.append(_make_test("36", str(count_divisors(36))))
    tests.append(_make_test("1000000", str(count_divisors(1000000))))
    tests.append(_make_test("999999937", str(count_divisors(999999937))))
    tests.append(_make_test("720720", str(count_divisors(720720))))
    tests.append(_make_test("1000000000", str(count_divisors(1000000000))))
    return tests

def _gen_tests_3_3():
    tests = []
    tests.append(_make_test("5", "15"))
    tests.append(_make_test("1", "1"))
    tests.append(_make_test("10", "55"))
    tests.append(_make_test("100", "5050"))
    tests.append(_make_test("0", "0"))
    tests.append(_make_test("1000000", str(1000000 * 1000001 // 2)))
    tests.append(_make_test("999999999", str(999999999 * 1000000000 // 2)))
    tests.append(_make_test("1000000000000", str(10**12 * (10**12 + 1) // 2)))
    tests.append(_make_test("999999999999999999", str(999999999999999999 * 10**18 // 2)))
    tests.append(_make_test("1000000000000000000", str(10**18 * (10**18 + 1) // 2)))
    return tests


STAGE_3_PROBLEMS = [
    {
        "id": "3_1",
        "stage_id": 3,
        "order": 1,
        "title": "In dãy số",
        "difficulty": "Khởi động",
        "time_limit": 1.0,
        "description": r"""## In dãy số từ 1 đến N

### Đề bài
Cho số nguyên dương $N$. In ra các số từ 1 đến $N$, mỗi số trên một dòng.

### Input
- Một dòng chứa số nguyên dương $N$ ($1 \le N \le 1000$).

### Output
- In $N$ dòng, dòng thứ $i$ chứa số $i$.

### Ví dụ
| Input | Output |
|-------|--------|
| `5` | `1`<br>`2`<br>`3`<br>`4`<br>`5` |

### Gợi ý
Dùng vòng lặp `for so_thu_tu in range(1, n+1)` và `print(so_thu_tu)`.
""",
    },
    {
        "id": "3_2",
        "stage_id": 3,
        "order": 2,
        "title": "Đếm số ước",
        "difficulty": "Vận dụng",
        "time_limit": 1.0,
        "description": r"""## Đếm số ước

### Đề bài
Cho số nguyên dương $N$. Đếm số ước dương của $N$.

Ước của $N$ là số nguyên dương $d$ sao cho $N$ chia hết cho $d$ ($N \mod d = 0$).

### Input
- Một dòng chứa số nguyên dương $N$ ($1 \le N \le 10^9$).

### Output
- In ra số lượng ước dương của $N$.

### Ví dụ
| Input | Output |
|-------|--------|
| `12` | `6` |
| `7` | `2` |

**Giải thích:** Các ước của 12 là: 1, 2, 3, 4, 6, 12 → có 6 ước.

### Gợi ý
Nếu duyệt từ 1 đến $N$ thì $O(N) = O(10^9)$ → TLE! Hãy chỉ duyệt đến $\sqrt{N}$: nếu $i$ là ước thì $N/i$ cũng là ước → $O(\sqrt{N})$.
""",
    },
    {
        "id": "3_3",
        "stage_id": 3,
        "order": 3,
        "title": "Tổng Gauss",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 1.0,
        "description": r"""## Tổng $1 + 2 + \ldots + N$

### Đề bài
Cho số nguyên không âm $N$. Tính tổng $S = 1 + 2 + 3 + \ldots + N$.

### Input
- Một dòng chứa số nguyên $N$ ($0 \le N \le 10^{18}$).

### Output
- In ra tổng $S$.

### Ví dụ
| Input | Output |
|-------|--------|
| `5` | `15` |
| `100` | `5050` |

### ⚠️ Cảnh báo
$N$ lên tới $10^{18}$! Vòng lặp sẽ chạy mãi không xong. Em **bắt buộc** phải dùng công thức toán học $S = \dfrac{N(N+1)}{2}$ để giải trong $O(1)$.
""",
    },
]

# ============================================================================
# CHẶNG 4: XỬ LÝ XÂU KÝ TỰ (STRING)
# ============================================================================

STAGE_4_THEORY = r"""
# 📝 Chặng 4: Xử lý Xâu ký tự (String)

## 1. Xâu (String) là gì?

Xâu là một **dãy các ký tự** liên tiếp. Trong Python, xâu đặt trong nháy đơn `'...'` hoặc nháy kép `"..."`.

```python
ten_hoc_sinh = "Nguyễn Văn An"
khau_hieu = 'HSG Python 2024'
xau_rong = ""              # Xâu rỗng — không có ký tự nào

# Độ dài xâu
do_dai = len(ten_hoc_sinh)     # 13

# Truy cập từng ký tự — đếm từ 0!
ky_tu_dau = ten_hoc_sinh[0]    # 'N'   (ký tự đầu tiên)
ky_tu_cuoi = ten_hoc_sinh[-1]  # 'n'   (ký tự cuối = -1)
ky_tu_thu_3 = ten_hoc_sinh[2]  # 'u'   (ký tự thứ 3, tính từ 0)
```

### Duyệt từng ký tự:
```python
xau_can_xu_ly = "abcdef"

# Cách 1: Duyệt trực tiếp từng ký tự
for ky_tu in xau_can_xu_ly:
    print(ky_tu)    # In lần lượt: a, b, c, d, e, f

# Cách 2: Duyệt bằng chỉ số (khi cần biết vị trí)
for vi_tri in range(len(xau_can_xu_ly)):
    print(f"Vị trí {vi_tri}: {xau_can_xu_ly[vi_tri]}")
```

## 2. Cắt xâu (Slicing) — Siêu năng lực của Python

Cú pháp: `xau[bat_dau : ket_thuc : buoc_nhay]`

```python
xau_goc = "abcdefgh"

# Lấy đoạn từ vị trí 2 đến 4 (không bao gồm 5)
doan_giua = xau_goc[2:5]        # "cde"

# Lấy 3 ký tự đầu
phan_dau = xau_goc[:3]          # "abc"

# Lấy từ vị trí 5 đến hết
phan_cuoi = xau_goc[5:]         # "fgh"

# Lấy cách 1 ký tự
xau_cach_1 = xau_goc[::2]       # "aceg"

# ĐẢO NGƯỢC XÂU — dùng nhiều trong thi HSG!
xau_nguoc = xau_goc[::-1]       # "hgfedcba"
```

## 3. Các hàm xử lý xâu quan trọng nhất

```python
cau_van = "Python rất hay, Python rất vui"

# Đếm số lần xuất hiện của một chuỗi con
so_lan_python = cau_van.count("Python")    # 2

# Chuyển thành chữ HOA
chu_hoa = cau_van.upper()    # "PYTHON RẤT HAY, PYTHON RẤT VUI"

# Chuyển thành chữ thường
chu_thuong = cau_van.lower()    # "python rất hay, python rất vui"

# Thay thế chuỗi con
cau_moi = cau_van.replace("Python", "HSG")
# "HSG rất hay, HSG rất vui"

# Tách xâu thành danh sách các từ
danh_sach_tu = cau_van.split(", ")
# ["Python rất hay", "Python rất vui"]

# Nối danh sách thành xâu
xau_noi = " - ".join(["An", "Bình", "Chi"])
# "An - Bình - Chi"

# Tìm vị trí xuất hiện đầu tiên (-1 nếu không tìm thấy)
vi_tri = cau_van.find("hay")    # 12
```

## 4. Bảng mã ASCII — `ord()` và `chr()`

Mỗi ký tự được máy tính lưu dưới dạng số nguyên:

```python
# ord() — Lấy mã ASCII của ký tự
ma_A = ord('A')    # 65
ma_a = ord('a')    # 97
ma_0 = ord('0')    # 48
ma_Z = ord('Z')    # 90

# chr() — Chuyển mã ASCII thành ký tự
ky_tu_65 = chr(65)    # 'A'
ky_tu_97 = chr(97)    # 'a'
```

### Bảng mã cần nhớ:

| Ký tự | Mã ASCII |
|-------|----------|
| `'A'` đến `'Z'` | 65 đến 90 |
| `'a'` đến `'z'` | 97 đến 122 |
| `'0'` đến `'9'` | 48 đến 57 |

### Ứng dụng — Mã hóa Caesar (dịch ký tự):
```python
ky_tu_goc = 'A'
buoc_dich = 3    # Dịch 3 vị trí

# Dịch 'A' → 'D'
ky_tu_moi = chr((ord(ky_tu_goc) - ord('A') + buoc_dich) % 26 + ord('A'))
print(ky_tu_moi)    # 'D'
```
"""

STAGE_4_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `s[::-1]`, `.split()`, `.join()` và `.count()`

### Vũ khí 1: Đảo ngược xâu `xau[::-1]`

| Thuộc tính | Chi tiết |
|---|---|
| **Cú pháp** | `xau[::-1]` |
| **Cách hoạt động** | Tạo xâu mới bằng cách đọc từ cuối về đầu. Chạy ở tầng C, cực nhanh. |
| **Độ phức tạp** | $O(N)$ — nhưng nhanh hơn tự viết vòng lặp rất nhiều |

```python
xau_goc = "abcdef"

# ❌ Cách chậm — tự viết vòng lặp (còn bị lỗi hiệu năng)
xau_nguoc = ""
for vi_tri in range(len(xau_goc) - 1, -1, -1):
    xau_nguoc += xau_goc[vi_tri]   # Mỗi += tạo xâu mới → O(N²)!

# ✅ Cách nhanh — slicing C-level, thực sự O(N)
xau_nguoc = xau_goc[::-1]    # "fedcba"
```

### Vũ khí 2: `.split()` và `' '.join()`

```python
chuoi_nhap = "3 1 4 1 5 9 2 6"

# Tách thành danh sách
danh_sach = chuoi_nhap.split()    # ["3", "1", "4", ...]

# Chuyển thành số và xử lý
danh_sach_so = list(map(int, danh_sach.split()))

# Nối lại thành chuỗi
chuoi_ket_qua = " ".join(map(str, danh_sach_so))
```

### Vũ khí 3: `.count()` — Đếm siêu tốc

```python
xau_can_dem = "abracadabra"

# ❌ Tự đếm bằng vòng lặp
dem_a_vong_lap = 0
for ky_tu in xau_can_dem:
    if ky_tu == 'a':
        dem_a_vong_lap += 1

# ✅ Dùng .count() — 1 dòng, chạy ở tầng C
dem_a_nhanh = xau_can_dem.count('a')    # 5
```
"""

def _gen_tests_4_1():
    tests = []
    tests.append(_make_test("abracadabra\na", "5"))
    tests.append(_make_test("hello\nl", "2"))
    tests.append(_make_test("aaaa\na", "4"))
    tests.append(_make_test("xyz\nw", "0"))
    tests.append(_make_test("aAbBaA\na", "2"))
    tests.append(_make_test("a\na", "1"))
    tests.append(_make_test("abcdefghij\ne", "1"))
    random.seed(301)
    for do_dai in [1000, 10000, 100000]:
        xau = ''.join(random.choices('abcdefghij', k=do_dai))
        ky_tu_dem = 'a'
        so_lan = xau.count(ky_tu_dem)
        tests.append(_make_test(f"{xau}\n{ky_tu_dem}", str(so_lan)))
    return tests

def _gen_tests_4_2():
    tests = []
    tests.append(_make_test("aba", "YES"))
    tests.append(_make_test("abba", "YES"))
    tests.append(_make_test("abc", "NO"))
    tests.append(_make_test("a", "YES"))
    tests.append(_make_test("ab", "NO"))
    tests.append(_make_test("abacaba", "YES"))
    tests.append(_make_test("racecar", "YES"))
    random.seed(401)
    nua_xau = ''.join(random.choices('abcdef', k=50000))
    xau_palindrome = nua_xau + nua_xau[::-1]
    tests.append(_make_test(xau_palindrome, "YES"))
    xau_ngau_nhien = ''.join(random.choices('abcdef', k=100000))
    ket_qua = "YES" if xau_ngau_nhien == xau_ngau_nhien[::-1] else "NO"
    tests.append(_make_test(xau_ngau_nhien, ket_qua))
    nua_le = ''.join(random.choices('abc', k=50000))
    xau_palindrome_le = nua_le + 'x' + nua_le[::-1]
    tests.append(_make_test(xau_palindrome_le, "YES"))
    return tests

def _gen_tests_4_3():
    tests = []
    tests.append(_make_test("Hello World", "2"))
    tests.append(_make_test("Python", "1"))
    tests.append(_make_test("  Hello   World  ", "2"))
    tests.append(_make_test("a b c d e", "5"))
    tests.append(_make_test("   ", "0"))
    tests.append(_make_test("one", "1"))
    tests.append(_make_test("the quick brown fox jumps over the lazy dog", "9"))
    random.seed(501)
    cac_tu = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta']
    for so_tu in [10000, 50000, 100000]:
        van_ban = ' '.join(random.choices(cac_tu, k=so_tu))
        tests.append(_make_test(van_ban, str(so_tu)))
    return tests


STAGE_4_PROBLEMS = [
    {
        "id": "4_1",
        "stage_id": 4,
        "order": 1,
        "title": "Đếm ký tự",
        "difficulty": "Khởi động",
        "time_limit": 1.0,
        "description": r"""## Đếm ký tự

### Đề bài
Cho xâu $s$ và ký tự $c$. Đếm số lần ký tự $c$ xuất hiện trong xâu $s$ (phân biệt hoa thường).

### Input
- Dòng 1: Xâu $s$ (chỉ chứa chữ cái tiếng Anh, $1 \le |s| \le 10^5$).
- Dòng 2: Ký tự $c$.

### Output
- In ra số lần ký tự $c$ xuất hiện trong $s$.

### Ví dụ
| Input | Output |
|-------|--------|
| `abracadabra`<br>`a` | `5` |
| `hello`<br>`l` | `2` |

### Gợi ý
Dùng phương thức `.count()` của xâu — chỉ cần 1 dòng!
""",
    },
    {
        "id": "4_2",
        "stage_id": 4,
        "order": 2,
        "title": "Kiểm tra Palindrome",
        "difficulty": "Vận dụng",
        "time_limit": 1.0,
        "description": r"""## Kiểm tra Palindrome

### Đề bài
Cho xâu $s$. Kiểm tra xem $s$ có phải là **palindrome** không (đọc xuôi và đọc ngược giống nhau).

### Input
- Một dòng chứa xâu $s$ (chỉ chứa chữ cái thường, $1 \le |s| \le 10^5$).

### Output
- In `YES` nếu $s$ là palindrome, `NO` nếu không phải.

### Ví dụ
| Input | Output |
|-------|--------|
| `aba` | `YES` |
| `abc` | `NO` |
| `abba` | `YES` |

### Gợi ý
Nhớ Vũ Khí: `s[::-1]` đảo ngược xâu tức thì! So sánh `s == s[::-1]`.
""",
    },
    {
        "id": "4_3",
        "stage_id": 4,
        "order": 3,
        "title": "Đếm từ",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 1.0,
        "description": r"""## Đếm số từ

### Đề bài
Cho một đoạn văn bản. Đếm số từ trong đoạn văn bản đó. Các từ được ngăn cách bởi một hoặc nhiều dấu cách.

### Input
- Một dòng chứa đoạn văn bản (chỉ chứa chữ cái và dấu cách, $0 \le$ độ dài $\le 10^6$).

### Output
- In ra số từ trong đoạn văn bản. Nếu đoạn văn bản rỗng hoặc chỉ có dấu cách, in `0`.

### Ví dụ
| Input | Output |
|-------|--------|
| `Hello World` | `2` |
| `  Hello   World  ` | `2` |
| `Python` | `1` |

### Gợi ý
Phương thức `.split()` (không đối số) tự động bỏ qua dấu cách thừa và trả về danh sách các từ. Đếm bằng `len()`.
""",
    },
]


# ============================================================================
# CHẶNG 5: DANH SÁCH (LIST) & TẬP HỢP (SET/DICT)
# ============================================================================

STAGE_5_THEORY = r"""
# 📊 Chặng 5: Danh sách (List) & Tập hợp (Set/Dict)

## 1. Danh sách (List) — Mảng trong Python

List giống như một **dãy số** (mảng), nhưng linh hoạt hơn nhiều. Đây là cấu trúc dữ liệu quan trọng nhất trong thi HSG.

```python
# Tạo danh sách
diem_cac_mon = [9, 8, 7, 10, 6]
ten_hoc_sinh = ["An", "Bình", "Chi", "Dũng"]
danh_sach_rong = []

# Truy cập phần tử (đếm từ 0!)
diem_dau = diem_cac_mon[0]      # 9  (phần tử đầu tiên)
diem_cuoi = diem_cac_mon[-1]    # 6  (phần tử cuối)
diem_thu_3 = diem_cac_mon[2]    # 7  (phần tử thứ 3)

# Độ dài
so_mon_hoc = len(diem_cac_mon)  # 5

# Thêm phần tử vào cuối
diem_cac_mon.append(9)          # [9, 8, 7, 10, 6, 9]
```

### Đọc mảng từ input:
```python
so_phan_tu = int(input())
mang_so = list(map(int, input().split()))

# Duyệt mảng
for gia_tri in mang_so:
    print(gia_tri)
```

## 2. List Comprehension — Viết vòng lặp cực ngắn

Đây là cách Python cho phép viết vòng lặp tạo danh sách trong **1 dòng**:

```python
so_phan_tu = 10

# Tạo danh sách bình phương các số từ 1 đến 10
binh_phuong = [so**2 for so in range(1, 11)]
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# Lọc chỉ lấy số chẵn
so_chan = [so for so in range(1, 21) if so % 2 == 0]
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Đọc n dòng, mỗi dòng 1 số
cac_so = [int(input()) for _ in range(so_phan_tu)]
```

## 3. Set — Tập hợp (Không có phần tử trùng, tra cứu $O(1)$)

Set là cấu trúc dữ liệu lưu các phần tử **không trùng nhau** và cho phép kiểm tra phần tử trong $O(1)$ (cực nhanh!).

```python
# Tạo set
tap_hop_so = {1, 2, 3, 4, 5}
tap_hop_tu_list = set([1, 2, 2, 3, 3, 3])    # {1, 2, 3} — tự loại trùng!

# Kiểm tra phần tử
so_can_tim = 3
if so_can_tim in tap_hop_so:       # O(1) — cực nhanh!
    print("Có trong tập hợp")

# So sánh với list (chậm hơn nhiều!)
danh_sach = [1, 2, 3, 4, 5]
if so_can_tim in danh_sach:        # O(N) — duyệt từ đầu đến cuối!
    print("Có trong danh sách")
```

### Tại sao set nhanh hơn list?

- **List**: Tìm kiếm = duyệt tuần tự từ đầu → cuối → $O(N)$
- **Set**: Dùng **bảng băm (hash table)** → tra cứu tức thì → $O(1)$

## 4. Dict — Từ điển (Ánh xạ Khóa → Giá trị)

Dict lưu cặp `khóa: giá trị`, tra cứu theo khóa trong $O(1)$:

```python
# Đếm tần suất xuất hiện của từng số
danh_sach_so = [1, 2, 2, 3, 3, 3, 1]
tan_suat = {}

for so in danh_sach_so:
    if so in tan_suat:
        tan_suat[so] += 1
    else:
        tan_suat[so] = 1
# tan_suat = {1: 2, 2: 2, 3: 3}

# Truy cập giá trị
print(tan_suat[3])           # 3
print(tan_suat.get(5, 0))    # 0 (mặc định nếu key không có)
```
"""

STAGE_5_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `set`, `collections.Counter` và tra cứu $O(1)$

### Vũ khí 1: `set` — Tra cứu $O(1)$ thay vì $O(N)$

| Thuộc tính | Chi tiết |
|---|---|
| **Cú pháp** | `tap_hop = set(danh_sach)` |
| **Tra cứu** | `phan_tu in tap_hop` → $O(1)$ |
| **So sánh** | `phan_tu in danh_sach` → $O(N)$ — chậm hơn hàng triệu lần khi N lớn! |

```python
so_phan_tu = 1000000
danh_sach = list(range(so_phan_tu))
tap_hop = set(danh_sach)

# ❌ Tra cứu trong list: O(N) mỗi lần → O(N²) tổng
for so_can_tim in range(so_phan_tu):
    if so_can_tim in danh_sach:    # Rất chậm!
        pass

# ✅ Tra cứu trong set: O(1) mỗi lần → O(N) tổng
for so_can_tim in range(so_phan_tu):
    if so_can_tim in tap_hop:      # Nhanh như chớp!
        pass
```

### Vũ khí 2: `collections.Counter` — Đếm tần suất trong 1 dòng

| Thuộc tính | Chi tiết |
|---|---|
| **Tên** | `Counter` từ module `collections` |
| **Cú pháp** | `from collections import Counter` rồi `Counter(danh_sach)` |
| **Cách hoạt động** | Duyệt danh sách 1 lần, đếm số lần xuất hiện của từng phần tử, chạy ở tầng C |
| **Độ phức tạp** | $O(N)$ |

```python
from collections import Counter

danh_sach_so = [1, 2, 2, 3, 3, 3, 1]

# ❌ Tự đếm thủ công
tan_suat_thu_cong = {}
for so in danh_sach_so:
    tan_suat_thu_cong[so] = tan_suat_thu_cong.get(so, 0) + 1

# ✅ Dùng Counter — 1 dòng!
tan_suat_nhanh = Counter(danh_sach_so)
# Counter({3: 3, 1: 2, 2: 2})

# Tìm phần tử xuất hiện nhiều nhất
phan_tu_nhieu_nhat = tan_suat_nhanh.most_common(1)[0]
# (3, 3) — số 3 xuất hiện 3 lần
```
"""

def _gen_tests_5_1():
    tests = []
    tests.append(_make_test("5\n3 1 4 1 5", "5"))
    tests.append(_make_test("1\n42", "42"))
    tests.append(_make_test("3\n-1 -2 -3", "-1"))
    tests.append(_make_test("4\n0 0 0 0", "0"))
    tests.append(_make_test("5\n-5 -4 -3 -2 -1", "-1"))
    tests.append(_make_test("3\n1000000000 999999999 1", "1000000000"))
    tests.append(_make_test("2\n-1000000000 1000000000", "1000000000"))
    random.seed(601)
    for so_luong in [100000, 500000, 1000000]:
        mang = [random.randint(-10**9, 10**9) for _ in range(so_luong)]
        gia_tri_lon_nhat = max(mang)
        tests.append(_make_test(f"{so_luong}\n{' '.join(map(str, mang))}", str(gia_tri_lon_nhat)))
    return tests

def _gen_tests_5_2():
    tests = []
    tests.append(_make_test("5\n1 2 2 3 3", "2"))
    tests.append(_make_test("1\n5", "5"))
    tests.append(_make_test("7\n1 1 1 2 2 3 3", "1"))
    tests.append(_make_test("4\n4 4 4 4", "4"))
    tests.append(_make_test("6\n3 3 2 2 1 1", "1"))
    tests.append(_make_test("5\n5 4 3 2 1", "1"))
    tests.append(_make_test("3\n-1 -1 2", "-1"))
    random.seed(701)
    for so_luong in [100000, 500000, 1000000]:
        cac_gia_tri = list(range(1, 101))
        mang = [random.choice(cac_gia_tri) for _ in range(so_luong)]
        dem = Counter(mang)
        tan_suat_cao_nhat = max(dem.values())
        cac_ung_vien = [k for k, v in dem.items() if v == tan_suat_cao_nhat]
        ket_qua = min(cac_ung_vien)
        tests.append(_make_test(f"{so_luong}\n{' '.join(map(str, mang))}", str(ket_qua)))
    return tests

def _gen_tests_5_3():
    tests = []
    tests.append(_make_test("5\n1 2 3 4 5", "5"))
    tests.append(_make_test("5\n1 1 1 1 1", "1"))
    tests.append(_make_test("1\n42", "1"))
    tests.append(_make_test("6\n1 2 1 2 1 2", "2"))
    tests.append(_make_test("4\n0 0 0 0", "1"))
    tests.append(_make_test("5\n-1 0 1 -1 0", "3"))
    tests.append(_make_test("3\n1000000 -1000000 0", "3"))
    random.seed(801)
    for so_luong in [100000, 500000, 1000000]:
        mang = [random.randint(1, so_luong // 2) for _ in range(so_luong)]
        ket_qua = len(set(mang))
        tests.append(_make_test(f"{so_luong}\n{' '.join(map(str, mang))}", str(ket_qua)))
    return tests


STAGE_5_PROBLEMS = [
    {
        "id": "5_1",
        "stage_id": 5,
        "order": 1,
        "title": "Giá trị lớn nhất",
        "difficulty": "Khởi động",
        "time_limit": 1.0,
        "description": r"""## Giá trị lớn nhất trong mảng

### Đề bài
Cho mảng $N$ số nguyên. Tìm giá trị lớn nhất.

### Input
- Dòng 1: Số nguyên $N$ ($1 \le N \le 10^6$).
- Dòng 2: $N$ số nguyên $a_1, a_2, \ldots, a_N$ ($|a_i| \le 10^9$).

### Output
- In ra giá trị lớn nhất trong mảng.

### Ví dụ
| Input | Output |
|-------|--------|
| `5`<br>`3 1 4 1 5` | `5` |
| `3`<br>`-1 -2 -3` | `-1` |

### Gợi ý
Dùng hàm `max()` — chỉ cần 1 dòng!
""",
    },
    {
        "id": "5_2",
        "stage_id": 5,
        "order": 2,
        "title": "Phần tử xuất hiện nhiều nhất",
        "difficulty": "Vận dụng",
        "time_limit": 1.5,
        "description": r"""## Phần tử xuất hiện nhiều nhất

### Đề bài
Cho mảng $N$ số nguyên. Tìm phần tử xuất hiện nhiều lần nhất. Nếu có nhiều phần tử cùng tần suất cao nhất, in ra phần tử nhỏ nhất.

### Input
- Dòng 1: Số nguyên $N$ ($1 \le N \le 10^6$).
- Dòng 2: $N$ số nguyên $a_1, \ldots, a_N$ ($|a_i| \le 10^9$).

### Output
- In ra phần tử xuất hiện nhiều nhất (nhỏ nhất nếu hòa).

### Ví dụ
| Input | Output |
|-------|--------|
| `7`<br>`1 1 1 2 2 3 3` | `1` |
| `5`<br>`1 2 2 3 3` | `2` |

### Gợi ý
Dùng `collections.Counter` để đếm tần suất trong 1 dòng, rồi tìm phần tử có tần suất cao nhất.
""",
    },
    {
        "id": "5_3",
        "stage_id": 5,
        "order": 3,
        "title": "Đếm phần tử phân biệt",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 1.0,
        "description": r"""## Đếm phần tử phân biệt

### Đề bài
Cho mảng $N$ số nguyên. Đếm số lượng giá trị **phân biệt** (khác nhau) trong mảng.

### Input
- Dòng 1: Số nguyên $N$ ($1 \le N \le 10^6$).
- Dòng 2: $N$ số nguyên $a_1, \ldots, a_N$ ($|a_i| \le 10^9$).

### Output
- In ra số lượng giá trị phân biệt.

### Ví dụ
| Input | Output |
|-------|--------|
| `5`<br>`1 2 3 4 5` | `5` |
| `5`<br>`1 1 1 1 1` | `1` |

### Gợi ý
Chuyển list thành set sẽ tự loại bỏ trùng, rồi đếm bằng `len()` → $O(N)$. Cách dùng 2 vòng lặp lồng nhau sẽ là $O(N^2)$ → TLE!
""",
    },
]


# ============================================================================
# CHẶNG 6: SỐ HỌC TRONG ĐỀ THI HSG
# ============================================================================

STAGE_6_THEORY = r"""
# 🔢 Chặng 6: Số học trong đề thi HSG

## 1. Số nguyên tố là gì?

Số nguyên tố là số tự nhiên **lớn hơn 1** và **chỉ chia hết cho 1 và chính nó**.

- Là nguyên tố: 2, 3, 5, 7, 11, 13, 17, 19, 23...
- Không phải nguyên tố: 1 (vì nhỏ hơn 2), 4 (= 2×2), 6 (= 2×3), 9 (= 3×3)...

### Kiểm tra nguyên tố — Cách ngây thơ $O(N)$:

```python
so_can_kiem_tra = int(input())

# Duyệt từ 2 đến N-1 — với N lớn sẽ rất chậm!
la_nguyen_to = True
if so_can_kiem_tra < 2:
    la_nguyen_to = False
else:
    for uoc_chia in range(2, so_can_kiem_tra):
        if so_can_kiem_tra % uoc_chia == 0:
            la_nguyen_to = False
            break

print("YES" if la_nguyen_to else "NO")
```

### Kiểm tra nguyên tố — Cách tối ưu $O(\sqrt{N})$:

> 💡 **Nhận xét quan trọng:** Nếu $N$ có ước $d > \sqrt{N}$, thì $N/d < \sqrt{N}$ cũng là ước. Vậy chỉ cần kiểm tra đến $\sqrt{N}$!

```python
import math

def kiem_tra_nguyen_to(so_can_kiem_tra):
    if so_can_kiem_tra < 2:
        return False
    if so_can_kiem_tra < 4:       # 2 và 3 là nguyên tố
        return True
    if so_can_kiem_tra % 2 == 0 or so_can_kiem_tra % 3 == 0:
        return False              # Loại bội của 2 và 3

    # Chỉ kiểm tra đến căn bậc 2 của N
    uoc_chia = 5
    while uoc_chia <= math.isqrt(so_can_kiem_tra):
        if so_can_kiem_tra % uoc_chia == 0:
            return False
        if so_can_kiem_tra % (uoc_chia + 2) == 0:
            return False
        uoc_chia += 6    # Bước nhảy 6 để bỏ qua bội của 2 và 3
    return True

so = int(input())
print("YES" if kiem_tra_nguyen_to(so) else "NO")
```

## 2. Sàng nguyên tố Eratosthenes

Khi cần tìm **TẤT CẢ** số nguyên tố từ 2 đến $N$, dùng sàng:

```python
import math

def sang_nguyen_to(gioi_han):
    # Tạo mảng, ban đầu giả sử tất cả đều là nguyên tố
    la_nguyen_to = [True] * (gioi_han + 1)
    la_nguyen_to[0] = la_nguyen_to[1] = False    # 0 và 1 không phải nguyên tố

    for so in range(2, math.isqrt(gioi_han) + 1):
        if la_nguyen_to[so]:
            # Đánh dấu tất cả bội của 'so' từ so² là hợp số
            for boi_so in range(so * so, gioi_han + 1, so):
                la_nguyen_to[boi_so] = False

    return la_nguyen_to

# Tìm tất cả số nguyên tố đến 1000
ket_qua = sang_nguyen_to(1000)
cac_nguyen_to = [so for so in range(2, 1001) if ket_qua[so]]
```

Độ phức tạp: $O(N \log \log N)$ — gần như tuyến tính!

## 3. ƯCLN và BCNN

- **ƯCLN (Ước Chung Lớn Nhất)**: Số lớn nhất chia hết cả $a$ và $b$
- **BCNN (Bội Chung Nhỏ Nhất)**: Số nhỏ nhất chia hết cho cả $a$ và $b$
- **Công thức liên hệ:** $BCNN(a, b) = \dfrac{a \times b}{UCLN(a, b)}$

```python
import math

so_a, so_b = map(int, input().split())

# Tính ƯCLN — thuật toán Euclid (cực nhanh!)
ucln = math.gcd(so_a, so_b)

# Tính BCNN
bcnn = so_a * so_b // ucln

print(ucln, bcnn)
```

### Thuật toán Euclid hoạt động thế nào?

```
gcd(12, 8):
  12 = 8 × 1 + 4  → gcd(8, 4)
  8  = 4 × 2 + 0  → gcd(4, 0) = 4
Vậy gcd(12, 8) = 4
```
"""

STAGE_6_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `math.isqrt()`, `math.gcd()`, `math.lcm()`

### Vũ khí 1: `math.isqrt(so)` — Căn bậc 2 nguyên, CHÍNH XÁC tuyệt đối

| Thuộc tính | Chi tiết |
|---|---|
| **Tên hàm** | `math.isqrt(n)` |
| **Cú pháp** | `math.isqrt(100)` → `10` |
| **Tại sao không dùng `int(n**0.5)`?** | Vì số thực có sai số — `int(n**0.5)` có thể trả về sai khi N lớn! |

```python
import math

so_kiem_tra = 10**18   # N rất lớn

# ❌ Có thể SAI do sai số float!
can_bac_2_sai = int(so_kiem_tra ** 0.5)

# ✅ Luôn ĐÚNG — chính xác tuyệt đối
can_bac_2_dung = math.isqrt(so_kiem_tra)
```

### Vũ khí 2: `math.gcd(a, b)` — ƯCLN tức thì

| Thuộc tính | Chi tiết |
|---|---|
| **Tên hàm** | `math.gcd(a, b)` |
| **Cách hoạt động** | Thuật toán Euclid ở tầng C |
| **Độ phức tạp** | $O(\log(\min(a, b)))$ — cực nhanh |

### Vũ khí 3: `math.lcm(a, b)` — BCNN (Python 3.9+)

```python
import math

so_a, so_b = 12, 8

ucln = math.gcd(so_a, so_b)    # 4
bcnn = math.lcm(so_a, so_b)    # 24

# Nếu Python < 3.9, tự tính:
bcnn_thu_cong = so_a * so_b // ucln    # 24
```
"""

def _gen_tests_6_1():
    def kiem_tra_nt(n):
        if n < 2: return False
        if n < 4: return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0: return False
            i += 6
        return True

    tests = []
    tests.append(_make_test("7", "YES"))
    tests.append(_make_test("1", "NO"))
    tests.append(_make_test("2", "YES"))
    tests.append(_make_test("4", "NO"))
    tests.append(_make_test("0", "NO"))
    tests.append(_make_test("97", "YES"))
    tests.append(_make_test("100", "NO"))
    tests.append(_make_test("999999937", "YES"))
    tests.append(_make_test("999999938", "NO"))
    tests.append(_make_test("1000000007", "YES"))
    return tests

def _gen_tests_6_2():
    tests = []
    tests.append(_make_test("12 8", "4 24"))
    tests.append(_make_test("7 5", "1 35"))
    tests.append(_make_test("6 6", "6 6"))
    tests.append(_make_test("1 1000000", "1 1000000"))
    tests.append(_make_test("100 75", f"{math.gcd(100,75)} {100*75//math.gcd(100,75)}"))
    tests.append(_make_test("17 13", "1 221"))
    tests.append(_make_test("1000000000 999999999",
                            f"{math.gcd(10**9, 10**9-1)} {10**9 * (10**9-1) // math.gcd(10**9, 10**9-1)}"))
    random.seed(901)
    for _ in range(3):
        a = random.randint(1, 10**9)
        b = random.randint(1, 10**9)
        g = math.gcd(a, b)
        l = a * b // g
        tests.append(_make_test(f"{a} {b}", f"{g} {l}"))
    return tests

def _gen_tests_6_3():
    def dem_nguyen_to(l, r):
        if r < 2: return 0
        l = max(l, 2)
        la_nguyen_to = [True] * (r + 1)
        la_nguyen_to[0] = la_nguyen_to[1] = False
        i = 2
        while i * i <= r:
            if la_nguyen_to[i]:
                for j in range(i * i, r + 1, i):
                    la_nguyen_to[j] = False
            i += 1
        return sum(1 for x in range(l, r + 1) if la_nguyen_to[x])

    tests = []
    tests.append(_make_test("1 10", str(dem_nguyen_to(1, 10))))
    tests.append(_make_test("2 2", "1"))
    tests.append(_make_test("1 1", "0"))
    tests.append(_make_test("10 20", str(dem_nguyen_to(10, 20))))
    tests.append(_make_test("1 100", str(dem_nguyen_to(1, 100))))
    tests.append(_make_test("100 200", str(dem_nguyen_to(100, 200))))
    tests.append(_make_test("1 1000", str(dem_nguyen_to(1, 1000))))
    tests.append(_make_test("1 100000", str(dem_nguyen_to(1, 100000))))
    tests.append(_make_test("1 1000000", str(dem_nguyen_to(1, 1000000))))
    tests.append(_make_test("1 5000000", str(dem_nguyen_to(1, 5000000))))
    return tests


STAGE_6_PROBLEMS = [
    {
        "id": "6_1",
        "stage_id": 6,
        "order": 1,
        "title": "Kiểm tra nguyên tố",
        "difficulty": "Khởi động",
        "time_limit": 1.0,
        "description": r"""## Kiểm tra số nguyên tố

### Đề bài
Cho số nguyên $N$. Kiểm tra $N$ có phải số nguyên tố không.

### Input
- Một dòng chứa số nguyên $N$ ($0 \le N \le 10^9 + 7$).

### Output
- In `YES` nếu $N$ là số nguyên tố, `NO` nếu không phải.

### Ví dụ
| Input | Output |
|-------|--------|
| `7` | `YES` |
| `4` | `NO` |
| `1` | `NO` |

### Gợi ý
Duyệt ước đến $\sqrt{N}$ bằng `math.isqrt(n)`. Lưu ý: 0 và 1 không phải số nguyên tố!
""",
    },
    {
        "id": "6_2",
        "stage_id": 6,
        "order": 2,
        "title": "ƯCLN và BCNN",
        "difficulty": "Vận dụng",
        "time_limit": 1.0,
        "description": r"""## ƯCLN và BCNN

### Đề bài
Cho hai số nguyên dương $a$ và $b$. Tìm ƯCLN và BCNN của chúng.

### Input
- Một dòng chứa hai số nguyên dương $a, b$ ($1 \le a, b \le 10^9$).

### Output
- In trên một dòng: ƯCLN và BCNN, cách nhau bởi dấu cách.

### Ví dụ
| Input | Output |
|-------|--------|
| `12 8` | `4 24` |
| `7 5` | `1 35` |

### Gợi ý
Dùng `math.gcd()` để tính ƯCLN. BCNN = $a \times b \div ƯCLN$.
""",
    },
    {
        "id": "6_3",
        "stage_id": 6,
        "order": 3,
        "title": "Đếm số nguyên tố trong đoạn",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 3.0,
        "description": r"""## Đếm số nguyên tố trong đoạn $[L, R]$

### Đề bài
Cho hai số nguyên dương $L$ và $R$. Đếm số lượng số nguyên tố trong đoạn $[L, R]$.

### Input
- Một dòng chứa hai số nguyên dương $L, R$ ($1 \le L \le R \le 5 \times 10^6$).

### Output
- In ra số lượng số nguyên tố trong đoạn $[L, R]$.

### Ví dụ
| Input | Output |
|-------|--------|
| `1 10` | `4` |
| `10 20` | `4` |

### Gợi ý
Với $R$ lên tới $5 \times 10^6$, kiểm tra từng số một sẽ chậm. Dùng **Sàng Eratosthenes** để tìm tất cả số nguyên tố đến $R$ trong $O(R \log \log R)$.
""",
    },
]


# ============================================================================
# CHẶNG 7: SẮP XẾP & TÌM KIẾM NHỊ PHÂN
# ============================================================================

STAGE_7_THEORY = r"""
# 📈 Chặng 7: Sắp xếp & Tìm kiếm nhị phân

## 1. Sắp xếp trong Python

Python dùng thuật toán **Timsort** — một thuật toán lai giữa Merge Sort và Insertion Sort, đạt $O(N \log N)$ trong mọi trường hợp và rất hiệu quả với dữ liệu thực tế.

```python
diem_hoc_sinh = [8, 5, 9, 3, 7, 6, 10, 4]

# Cách 1: sorted() — trả về danh sách MỚI, không thay đổi bản gốc
diem_sap_xep = sorted(diem_hoc_sinh)          # [3, 4, 5, 6, 7, 8, 9, 10]
print(diem_hoc_sinh)                          # Vẫn: [8, 5, 9, 3, 7, 6, 10, 4]

# Cách 2: .sort() — sắp xếp TRỰC TIẾP trên danh sách gốc
diem_hoc_sinh.sort()                          # diem_hoc_sinh bị thay đổi!

# Sắp xếp giảm dần
diem_giam_dan = sorted(diem_hoc_sinh, reverse=True)  # [10, 9, 8, 7, ...]
```

## 2. Sắp xếp theo điều kiện với `key=lambda`

Đây là kỹ thuật cực mạnh, cho phép sắp xếp theo bất kỳ tiêu chí nào:

```python
# Sắp xếp theo giá trị tuyệt đối
cac_so = [-5, 3, -1, 4, -2]
sap_xep_tuyet_doi = sorted(cac_so, key=lambda so: abs(so))
# Kết quả: [-1, -2, 3, 4, -5]

# Sắp xếp danh sách tên theo độ dài
danh_sach_ten = ["Nguyễn", "An", "Bình", "Chi"]
sap_xep_do_dai = sorted(danh_sach_ten, key=lambda ten: len(ten))
# Kết quả: ["An", "Chi", "Bình", "Nguyễn"]

# Sắp xếp học sinh: điểm cao trước, nếu bằng điểm thì tên tăng dần
hoc_sinh = [("An", 8), ("Bình", 9), ("Chi", 8), ("Dũng", 9)]
sap_xep_hs = sorted(hoc_sinh, key=lambda hs: (-hs[1], hs[0]))
# Kết quả: [("Bình", 9), ("Dũng", 9), ("An", 8), ("Chi", 8)]
```

### Giải thích `lambda`:
`lambda tham_so: bieu_thuc` là cách viết hàm ngắn gọn trong 1 dòng:
```python
# Hai cách viết tương đương:
key=lambda so: abs(so)

# Tương đương với:
def lay_gia_tri_sap_xep(so):
    return abs(so)
key=lay_gia_tri_sap_xep
```

## 3. Tìm kiếm nhị phân (Binary Search)

Khi mảng đã **sắp xếp rồi**, ta có thể tìm phần tử trong $O(\log N)$ thay vì $O(N)$!

### Ý tưởng:
Giống như tìm số trong quyển sổ có 1000 trang — thay vì lật từng trang, hãy mở ở trang giữa, nếu quá nhỏ thì tìm nửa sau, nếu quá lớn thì tìm nửa trước.

```python
def tim_kiem_nhi_phan(mang_da_sap_xep, gia_tri_can_tim):
    trai = 0
    phai = len(mang_da_sap_xep) - 1

    while trai <= phai:
        giua = (trai + phai) // 2    # Vị trí giữa

        if mang_da_sap_xep[giua] == gia_tri_can_tim:
            return giua              # Tìm thấy!
        elif mang_da_sap_xep[giua] < gia_tri_can_tim:
            trai = giua + 1          # Tìm ở nửa phải
        else:
            phai = giua - 1          # Tìm ở nửa trái

    return -1    # Không tìm thấy

mang = [1, 3, 5, 7, 9, 11, 13]
vi_tri = tim_kiem_nhi_phan(mang, 7)    # 3
```

### Dùng thư viện `bisect` — Nhanh và đã được tối ưu sẵn:

```python
import bisect

mang_da_sap = [1, 2, 4, 4, 4, 7, 9]

# bisect_left — Vị trí đầu tiên có thể chèn x (= vị trí phần tử >= x đầu tiên)
vi_tri_trai = bisect.bisect_left(mang_da_sap, 4)     # 2

# bisect_right — Vị trí sau cùng có thể chèn x
vi_tri_phai = bisect.bisect_right(mang_da_sap, 4)    # 5

# Đếm số lần 4 xuất hiện
so_lan_4 = vi_tri_phai - vi_tri_trai    # 3
```
"""

STAGE_7_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `sorted()` với `key=lambda`, `bisect`

### Vũ khí 1: `sorted()` / `.sort()` — Timsort $O(N \log N)$

| Thuộc tính | Chi tiết |
|---|---|
| **Tên hàm** | `sorted(iterable, key=..., reverse=...)` |
| **Cách hoạt động** | Timsort (C-level), ổn định (stable), $O(N \log N)$ trong mọi trường hợp |
| **Tham số `key`** | Hàm biến đổi mỗi phần tử trước khi so sánh. Dùng `lambda` để viết ngắn gọn |

### Vũ khí 2: `bisect` — Tìm kiếm nhị phân tốc độ cao

| Thuộc tính | Chi tiết |
|---|---|
| **Module** | `import bisect` |
| **`bisect_left(mang, x)`** | Vị trí đầu tiên có thể chèn $x$ |
| **`bisect_right(mang, x)`** | Vị trí cuối cùng có thể chèn $x$ |
| **Độ phức tạp** | $O(\log N)$ — cực nhanh trên mảng đã sắp xếp |

```python
import bisect

mang_da_sap = sorted([3, 1, 4, 1, 5, 9, 2, 6])
gia_tri_can_dem = 1

# ❌ Đếm tuần tự: O(N)
so_lan_cham = mang_da_sap.count(gia_tri_can_dem)

# ✅ Nhị phân: O(log N)
so_lan_nhanh = (bisect.bisect_right(mang_da_sap, gia_tri_can_dem)
               - bisect.bisect_left(mang_da_sap, gia_tri_can_dem))
```
"""

def _gen_tests_7_1():
    tests = []
    tests.append(_make_test("5\n3 1 4 1 5", "1 1 3 4 5"))
    tests.append(_make_test("1\n42", "42"))
    tests.append(_make_test("3\n3 2 1", "1 2 3"))
    tests.append(_make_test("4\n1 1 1 1", "1 1 1 1"))
    tests.append(_make_test("5\n5 4 3 2 1", "1 2 3 4 5"))
    tests.append(_make_test("3\n-1 0 1", "-1 0 1"))
    tests.append(_make_test("5\n-5 3 -1 4 -2", "-5 -2 -1 3 4"))
    random.seed(1001)
    for so_luong in [100000, 500000, 1000000]:
        mang = [random.randint(-10**9, 10**9) for _ in range(so_luong)]
        ket_qua = ' '.join(map(str, sorted(mang)))
        tests.append(_make_test(f"{so_luong}\n{' '.join(map(str, mang))}", ket_qua))
    return tests

def _gen_tests_7_2():
    tests = []
    def sap_xep_tuy_chinh(mang):
        return sorted(mang, key=lambda so: (abs(so), so))

    tests.append(_make_test("5\n-3 1 -1 4 2", ' '.join(map(str, sap_xep_tuy_chinh([-3,1,-1,4,2])))))
    tests.append(_make_test("3\n-1 0 1", ' '.join(map(str, sap_xep_tuy_chinh([-1,0,1])))))
    tests.append(_make_test("4\n5 -5 3 -3", ' '.join(map(str, sap_xep_tuy_chinh([5,-5,3,-3])))))
    tests.append(_make_test("1\n0", "0"))
    tests.append(_make_test("2\n-1000000000 1000000000", "-1000000000 1000000000"))
    tests.append(_make_test("3\n-2 -2 2", "-2 -2 2"))
    tests.append(_make_test("6\n6 -5 4 -3 2 -1", ' '.join(map(str, sap_xep_tuy_chinh([6,-5,4,-3,2,-1])))))
    random.seed(1101)
    for so_luong in [100000, 500000, 1000000]:
        mang = [random.randint(-10**9, 10**9) for _ in range(so_luong)]
        ket_qua = ' '.join(map(str, sap_xep_tuy_chinh(mang)))
        tests.append(_make_test(f"{so_luong}\n{' '.join(map(str, mang))}", ket_qua))
    return tests

def _gen_tests_7_3():
    import bisect
    tests = []
    def dem_xuat_hien(mang, gia_tri):
        mang_sap = sorted(mang)
        return bisect.bisect_right(mang_sap, gia_tri) - bisect.bisect_left(mang_sap, gia_tri)

    tests.append(_make_test("7 4\n1 2 4 4 4 7 9", "3"))
    tests.append(_make_test("5 3\n1 2 3 4 5", "1"))
    tests.append(_make_test("5 6\n1 2 3 4 5", "0"))
    tests.append(_make_test("1 1\n1", "1"))
    tests.append(_make_test("5 1\n1 1 1 1 1", "5"))
    tests.append(_make_test("4 0\n-1 0 0 1", "2"))
    tests.append(_make_test("6 -1\n-1 -1 -1 0 1 2", "3"))
    random.seed(1201)
    for so_luong in [100000, 500000, 1000000]:
        mang = [random.randint(1, 100) for _ in range(so_luong)]
        gia_tri_tim = random.randint(1, 100)
        ket_qua = mang.count(gia_tri_tim)
        tests.append(_make_test(f"{so_luong} {gia_tri_tim}\n{' '.join(map(str, mang))}", str(ket_qua)))
    return tests


STAGE_7_PROBLEMS = [
    {
        "id": "7_1",
        "stage_id": 7,
        "order": 1,
        "title": "Sắp xếp mảng",
        "difficulty": "Khởi động",
        "time_limit": 1.5,
        "description": r"""## Sắp xếp mảng tăng dần

### Đề bài
Cho mảng $N$ số nguyên. Sắp xếp mảng theo thứ tự tăng dần.

### Input
- Dòng 1: Số nguyên $N$ ($1 \le N \le 10^6$).
- Dòng 2: $N$ số nguyên $a_1, \ldots, a_N$ ($|a_i| \le 10^9$).

### Output
- In mảng đã sắp xếp, các số cách nhau bởi dấu cách.

### Ví dụ
| Input | Output |
|-------|--------|
| `5`<br>`3 1 4 1 5` | `1 1 3 4 5` |

### Gợi ý
Dùng `sorted()` hoặc `.sort()` — Timsort $O(N \log N)$.
""",
    },
    {
        "id": "7_2",
        "stage_id": 7,
        "order": 2,
        "title": "Sắp xếp theo giá trị tuyệt đối",
        "difficulty": "Vận dụng",
        "time_limit": 1.5,
        "description": r"""## Sắp xếp theo giá trị tuyệt đối

### Đề bài
Cho mảng $N$ số nguyên. Sắp xếp theo giá trị tuyệt đối tăng dần. Nếu hai số có cùng giá trị tuyệt đối, số âm đứng trước.

### Input
- Dòng 1: Số nguyên $N$ ($1 \le N \le 10^6$).
- Dòng 2: $N$ số nguyên $a_1, \ldots, a_N$ ($|a_i| \le 10^9$).

### Output
- In mảng đã sắp xếp, các số cách nhau bởi dấu cách.

### Ví dụ
| Input | Output |
|-------|--------|
| `5`<br>`-3 1 -1 4 2` | `-1 1 2 -3 4` |
| `4`<br>`5 -5 3 -3` | `-3 3 -5 5` |

### Gợi ý
Dùng `key=lambda so: (abs(so), so)` — sắp xếp theo giá trị tuyệt đối trước, nếu bằng thì theo giá trị gốc.
""",
    },
    {
        "id": "7_3",
        "stage_id": 7,
        "order": 3,
        "title": "Đếm số lần xuất hiện (Binary Search)",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 1.0,
        "description": r"""## Đếm số lần xuất hiện trong mảng

### Đề bài
Cho mảng $N$ số nguyên và một số $X$. Đếm số lần $X$ xuất hiện trong mảng.

### Input
- Dòng 1: Hai số nguyên $N$ và $X$ ($1 \le N \le 10^6$, $|X| \le 10^9$).
- Dòng 2: $N$ số nguyên.

### Output
- In ra số lần $X$ xuất hiện.

### Ví dụ
| Input | Output |
|-------|--------|
| `7 4`<br>`1 2 4 4 4 7 9` | `3` |
| `5 6`<br>`1 2 3 4 5` | `0` |

### Gợi ý
Sắp xếp mảng rồi dùng `bisect_left` và `bisect_right` → $O(N \log N)$ sắp xếp + $O(\log N)$ đếm.
""",
    },
]


# ============================================================================
# CHẶNG 8: PREFIX SUM, HAI CON TRỎ & ĐỆ QUY CÓ NHỚ
# ============================================================================

STAGE_8_THEORY = r"""
# ⚡ Chặng 8: Mảng cộng dồn (Prefix Sum), Hai con trỏ & Đệ quy có nhớ

## 1. Mảng cộng dồn (Prefix Sum)

### Bài toán: Tính tổng đoạn con $[l, r]$ nhiều lần

Cho mảng $N$ phần tử và $Q$ truy vấn, mỗi truy vấn hỏi tổng phần tử từ vị trí $l$ đến $r$.

```python
# Nếu mỗi truy vấn duyệt từ l đến r: O(N × Q) → TLE khi N, Q = 10^6
```

**Giải pháp:** Tính trước **mảng cộng dồn** — rồi mỗi truy vấn chỉ mất $O(1)$!

```python
import sys
input = sys.stdin.readline

so_phan_tu, so_truy_van = map(int, input().split())
mang_goc = list(map(int, input().split()))

# Bước 1: Xây dựng mảng cộng dồn
# prefix[i] = tổng của mang_goc[0] + mang_goc[1] + ... + mang_goc[i-1]
prefix = [0] * (so_phan_tu + 1)
for vi_tri in range(so_phan_tu):
    prefix[vi_tri + 1] = prefix[vi_tri] + mang_goc[vi_tri]

# Bước 2: Trả lời từng truy vấn trong O(1)
for _ in range(so_truy_van):
    vi_tri_trai, vi_tri_phai = map(int, input().split())
    # Tổng từ vị trí l đến r (đánh số từ 1)
    tong_doan = prefix[vi_tri_phai] - prefix[vi_tri_trai - 1]
    print(tong_doan)
```

### Hình dung trực quan:
```
mang_goc = [2, 5, 1, 4, 3]
prefix    = [0, 2, 7, 8, 12, 15]

Tổng từ vị trí 2 đến 4:
= prefix[4] - prefix[1]
= 12 - 2
= 10  (kiểm tra: 5 + 1 + 4 = 10 ✓)
```

## 2. Kỹ thuật Hai con trỏ (Two Pointers)

Dùng khi cần tìm **cặp phần tử** thỏa điều kiện trong mảng **đã sắp xếp**. Tiết kiệm từ $O(N^2)$ xuống $O(N)$!

```python
# Bài toán: Tìm 2 số trong mảng có tổng bằng K
mang_so = list(map(int, input().split()))
tong_can_tim = int(input())

mang_so.sort()    # PHẢI sắp xếp trước!

con_tro_trai = 0
con_tro_phai = len(mang_so) - 1

while con_tro_trai < con_tro_phai:
    tong_hien_tai = mang_so[con_tro_trai] + mang_so[con_tro_phai]

    if tong_hien_tai == tong_can_tim:
        print(mang_so[con_tro_trai], mang_so[con_tro_phai])
        break
    elif tong_hien_tai < tong_can_tim:
        con_tro_trai += 1    # Tổng nhỏ quá → tăng phần tử nhỏ
    else:
        con_tro_phai -= 1    # Tổng lớn quá → giảm phần tử lớn
else:
    print("NO")    # Không tìm thấy
```

## 3. Đệ quy có nhớ (Memoization)

Đệ quy thông thường thường tính lại cùng một giá trị nhiều lần → lãng phí. Đệ quy có nhớ **cache** kết quả lại!

### Ví dụ: Dãy Fibonacci

```python
from functools import lru_cache
import sys
sys.setrecursionlimit(200000)   # Tăng giới hạn đệ quy

# ❌ Đệ quy thông thường: O(2^N) — fib(40) mất hàng chục giây!
def fib_cham(vi_tri):
    if vi_tri <= 1:
        return vi_tri
    # Tính lại fib(vi_tri-2) rất nhiều lần!
    return fib_cham(vi_tri - 1) + fib_cham(vi_tri - 2)

# ✅ Đệ quy có nhớ: O(N) — fib(100000) chạy tức thì!
@lru_cache(None)    # None = cache không giới hạn
def fib_nhanh(vi_tri):
    if vi_tri <= 1:
        return vi_tri
    return fib_nhanh(vi_tri - 1) + fib_nhanh(vi_tri - 2)

vi_tri_can_tinh = int(input())
MOD = 10**9 + 7
print(fib_nhanh(vi_tri_can_tinh) % MOD)
```

### `@lru_cache(None)` hoạt động thế nào?

Khi gọi `fib_nhanh(10)`:
1. Lần đầu: tính toán và lưu vào cache
2. Lần sau: tra cache → trả về ngay, không tính lại!

Kết quả: Từ $O(2^N)$ xuống $O(N)$ — cực kỳ mạnh cho quy hoạch động!
"""

STAGE_8_WEAPON = r"""
## 🔫 Góc Vũ Khí Python: `itertools.accumulate` và `@lru_cache(None)`

### Vũ khí 1: `itertools.accumulate` — Prefix Sum trong 1 dòng

| Thuộc tính | Chi tiết |
|---|---|
| **Module** | `from itertools import accumulate` |
| **Cú pháp** | `list(accumulate(mang, initial=0))` |
| **Cách hoạt động** | Tạo mảng cộng dồn. Chạy ở tầng C, nhanh hơn viết vòng lặp |
| **Độ phức tạp** | $O(N)$ |

```python
from itertools import accumulate

mang_goc = [2, 5, 1, 4, 3]

# ❌ Tự viết vòng lặp
prefix_thu_cong = [0]
for gia_tri in mang_goc:
    prefix_thu_cong.append(prefix_thu_cong[-1] + gia_tri)

# ✅ Dùng accumulate — 1 dòng!
prefix_nhanh = list(accumulate(mang_goc, initial=0))
# [0, 2, 7, 8, 12, 15]

# Tổng từ vị trí l đến r (1-indexed):
# tong = prefix_nhanh[r] - prefix_nhanh[l-1]
```

### Vũ khí 2: `@functools.lru_cache(None)` — Cache đệ quy tự động

| Thuộc tính | Chi tiết |
|---|---|
| **Module** | `from functools import lru_cache` |
| **Cú pháp** | Thêm `@lru_cache(None)` ngay trên hàm đệ quy |
| **Cách hoạt động** | Tự cache kết quả. Gọi lại với cùng tham số → trả về ngay |
| **Độ phức tạp** | Giảm từ $O(2^N)$ xuống $O(N)$ cho bài Fibonacci! |

```python
from functools import lru_cache
import sys
sys.setrecursionlimit(200000)

@lru_cache(None)
def dem_cach(vi_tri, buoc_con_lai):
    if buoc_con_lai == 0:
        return 1 if vi_tri == 0 else 0
    if vi_tri < 0:
        return 0
    return dem_cach(vi_tri - 1, buoc_con_lai - 1) + dem_cach(vi_tri - 2, buoc_con_lai - 1)
```
"""

def _gen_tests_8_1():
    tests = []

    def tinh_tong_doan(mang, cac_truy_van):
        prefix = [0]
        for gia_tri in mang:
            prefix.append(prefix[-1] + gia_tri)
        ket_qua = []
        for l, r in cac_truy_van:
            ket_qua.append(str(prefix[r] - prefix[l - 1]))
        return '\n'.join(ket_qua)

    mang = [2, 5, 1, 4, 3]
    truy_van = [(1, 3), (2, 5)]
    du_lieu_vao = f"5 2\n{' '.join(map(str, mang))}\n1 3\n2 5"
    tests.append(_make_test(du_lieu_vao, tinh_tong_doan(mang, truy_van)))

    tests.append(_make_test("1 1\n42\n1 1", "42"))

    mang = [1, 1, 1, 1, 1]
    tests.append(_make_test(f"5 1\n{' '.join(map(str, mang))}\n1 5", "5"))

    mang = [-1, -2, -3, -4, -5]
    tests.append(_make_test(f"5 1\n{' '.join(map(str, mang))}\n1 5", "-15"))

    mang = [10, 20, 30]
    tests.append(_make_test(f"3 1\n{' '.join(map(str, mang))}\n2 2", "20"))

    mang = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    truy_van = [(1, 10), (3, 7), (5, 5)]
    du_lieu_vao = f"10 3\n{' '.join(map(str, mang))}\n1 10\n3 7\n5 5"
    tests.append(_make_test(du_lieu_vao, tinh_tong_doan(mang, truy_van)))

    mang = [0, 0, 0, 0, 0]
    tests.append(_make_test(f"5 1\n{' '.join(map(str, mang))}\n1 5", "0"))

    random.seed(1301)
    for so_phan_tu, so_truy_van in [(100000, 100000), (500000, 100000), (1000000, 100000)]:
        mang = [random.randint(-1000, 1000) for _ in range(so_phan_tu)]
        truy_van = []
        for _ in range(so_truy_van):
            l = random.randint(1, so_phan_tu)
            r = random.randint(l, min(l + 1000, so_phan_tu))
            truy_van.append((l, r))
        dong_du_lieu = [f"{so_phan_tu} {so_truy_van}", ' '.join(map(str, mang))]
        for l, r in truy_van:
            dong_du_lieu.append(f"{l} {r}")
        du_lieu_vao = '\n'.join(dong_du_lieu)
        tests.append(_make_test(du_lieu_vao, tinh_tong_doan(mang, truy_van)))
    return tests

def _gen_tests_8_2():
    tests = []

    def tim_cap(mang, tong_can_tim):
        mang_sap = sorted(mang)
        trai, phai = 0, len(mang_sap) - 1
        while trai < phai:
            tong = mang_sap[trai] + mang_sap[phai]
            if tong == tong_can_tim:
                return f"{mang_sap[trai]} {mang_sap[phai]}"
            elif tong < tong_can_tim:
                trai += 1
            else:
                phai -= 1
        return "NO"

    tests.append(_make_test("5 9\n2 7 11 15 1", tim_cap([2,7,11,15,1], 9)))
    tests.append(_make_test("4 6\n1 2 3 4", tim_cap([1,2,3,4], 6)))
    tests.append(_make_test("3 10\n1 2 3", "NO"))
    tests.append(_make_test("2 0\n-5 5", "-5 5"))
    tests.append(_make_test("5 0\n-3 -1 0 1 3", "-3 3"))
    tests.append(_make_test("4 4\n2 2 3 1", "1 3"))
    tests.append(_make_test("1 5\n5", "NO"))

    random.seed(1401)
    for so_luong in [100000, 500000, 1000000]:
        mang = sorted(random.sample(range(-so_luong, so_luong), min(so_luong, 2 * so_luong - 1)))
        if len(mang) >= 2:
            tong = mang[0] + mang[-1]
        else:
            tong = 0
        ket_qua = tim_cap(mang, tong)
        tests.append(_make_test(f"{len(mang)} {tong}\n{' '.join(map(str, mang))}", ket_qua))
    return tests

def _gen_tests_8_3():
    MOD = 10**9 + 7

    def fibonacci_mod(vi_tri):
        if vi_tri <= 1:
            return vi_tri
        so_truoc, so_hien_tai = 0, 1
        for _ in range(2, vi_tri + 1):
            so_truoc, so_hien_tai = so_hien_tai, (so_truoc + so_hien_tai) % MOD
        return so_hien_tai

    tests = []
    tests.append(_make_test("0", "0"))
    tests.append(_make_test("1", "1"))
    tests.append(_make_test("10", str(fibonacci_mod(10))))
    tests.append(_make_test("2", "1"))
    tests.append(_make_test("5", "5"))
    tests.append(_make_test("20", str(fibonacci_mod(20))))
    tests.append(_make_test("100", str(fibonacci_mod(100))))
    tests.append(_make_test("1000", str(fibonacci_mod(1000))))
    tests.append(_make_test("10000", str(fibonacci_mod(10000))))
    tests.append(_make_test("100000", str(fibonacci_mod(100000))))
    return tests


STAGE_8_PROBLEMS = [
    {
        "id": "8_1",
        "stage_id": 8,
        "order": 1,
        "title": "Tổng đoạn con (Prefix Sum)",
        "difficulty": "Khởi động",
        "time_limit": 2.0,
        "description": r"""## Tổng đoạn con

### Đề bài
Cho mảng $N$ số nguyên và $Q$ truy vấn. Mỗi truy vấn cho hai số $l, r$, hãy tính tổng các phần tử từ vị trí $l$ đến $r$ (đánh số từ 1).

### Input
- Dòng 1: Hai số $N, Q$ ($1 \le N, Q \le 10^6$).
- Dòng 2: $N$ số nguyên ($|a_i| \le 1000$).
- $Q$ dòng tiếp theo: Mỗi dòng hai số $l, r$ ($1 \le l \le r \le N$).

### Output
- $Q$ dòng, mỗi dòng là kết quả của một truy vấn.

### Ví dụ
| Input | Output |
|-------|--------|
| `5 2`<br>`2 5 1 4 3`<br>`1 3`<br>`2 5` | `8`<br>`13` |

### Gợi ý
Tính mảng prefix sum trước ($O(N)$), rồi mỗi truy vấn trả lời trong $O(1)$. Dùng `itertools.accumulate` để tạo prefix sum trong 1 dòng!
""",
    },
    {
        "id": "8_2",
        "stage_id": 8,
        "order": 2,
        "title": "Cặp có tổng bằng K",
        "difficulty": "Vận dụng",
        "time_limit": 1.5,
        "description": r"""## Tìm cặp có tổng bằng K

### Đề bài
Cho mảng $N$ số nguyên **phân biệt** và số $K$. Tìm hai phần tử có tổng bằng $K$.

### Input
- Dòng 1: Hai số $N, K$ ($1 \le N \le 10^6$, $|K| \le 2 \times 10^9$).
- Dòng 2: $N$ số nguyên phân biệt ($|a_i| \le 10^9$).

### Output
- Nếu tìm được, in hai số (nhỏ trước, lớn sau). Nếu không, in `NO`.
- Nếu có nhiều cặp, in cặp có số nhỏ nhất bé nhất.

### Ví dụ
| Input | Output |
|-------|--------|
| `5 9`<br>`2 7 11 15 1` | `2 7` |
| `3 10`<br>`1 2 3` | `NO` |

### Gợi ý
Sắp xếp mảng, dùng **hai con trỏ**: một ở đầu, một ở cuối. Nếu tổng nhỏ → tăng con trỏ trái, nếu lớn → giảm con trỏ phải.
""",
    },
    {
        "id": "8_3",
        "stage_id": 8,
        "order": 3,
        "title": "Fibonacci mod 10⁹+7",
        "difficulty": "HSG - Tối ưu",
        "time_limit": 1.0,
        "description": r"""## Fibonacci thứ N modulo $10^9 + 7$

### Đề bài
Tính số Fibonacci thứ $N$ modulo $10^9 + 7$.

Dãy Fibonacci: $F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)$.

### Input
- Một dòng chứa số nguyên $N$ ($0 \le N \le 10^5$).

### Output
- In ra $F(N) \mod (10^9 + 7)$.

### Ví dụ
| Input | Output |
|-------|--------|
| `0` | `0` |
| `1` | `1` |
| `10` | `55` |

### Gợi ý
Dùng đệ quy có nhớ `@lru_cache(None)` hoặc vòng lặp bottom-up. Nhớ tăng giới hạn đệ quy bằng `sys.setrecursionlimit()` nếu dùng đệ quy!
""",
    },
]


# ============================================================================
# TỔNG HỢP DỮ LIỆU TOÀN BỘ CURRICULUM
# ============================================================================

TEST_GENERATORS = {
    "1_1": _gen_tests_1_1,
    "1_2": _gen_tests_1_2,
    "1_3": _gen_tests_1_3,
    "2_1": _gen_tests_2_1,
    "2_2": _gen_tests_2_2,
    "2_3": _gen_tests_2_3,
    "3_1": _gen_tests_3_1,
    "3_2": _gen_tests_3_2,
    "3_3": _gen_tests_3_3,
    "4_1": _gen_tests_4_1,
    "4_2": _gen_tests_4_2,
    "4_3": _gen_tests_4_3,
    "5_1": _gen_tests_5_1,
    "5_2": _gen_tests_5_2,
    "5_3": _gen_tests_5_3,
    "6_1": _gen_tests_6_1,
    "6_2": _gen_tests_6_2,
    "6_3": _gen_tests_6_3,
    "7_1": _gen_tests_7_1,
    "7_2": _gen_tests_7_2,
    "7_3": _gen_tests_7_3,
    "8_1": _gen_tests_8_1,
    "8_2": _gen_tests_8_2,
    "8_3": _gen_tests_8_3,
}

STAGES = [
    {
        "id": 1,
        "title": "Làm quen Python & Nhập xuất chuẩn thi HSG",
        "icon": "🚀",
        "theory": STAGE_1_THEORY,
        "weapon": STAGE_1_WEAPON,
        "problems": STAGE_1_PROBLEMS,
    },
    {
        "id": 2,
        "title": "Rẽ nhánh & Toán học thông minh",
        "icon": "🔀",
        "theory": STAGE_2_THEORY,
        "weapon": STAGE_2_WEAPON,
        "problems": STAGE_2_PROBLEMS,
    },
    {
        "id": 3,
        "title": "Vòng lặp & Tư duy khử vòng lặp",
        "icon": "🔄",
        "theory": STAGE_3_THEORY,
        "weapon": STAGE_3_WEAPON,
        "problems": STAGE_3_PROBLEMS,
    },
    {
        "id": 4,
        "title": "Xử lý Xâu ký tự (String)",
        "icon": "📝",
        "theory": STAGE_4_THEORY,
        "weapon": STAGE_4_WEAPON,
        "problems": STAGE_4_PROBLEMS,
    },
    {
        "id": 5,
        "title": "Danh sách (List) & Tập hợp (Set/Dict)",
        "icon": "📊",
        "theory": STAGE_5_THEORY,
        "weapon": STAGE_5_WEAPON,
        "problems": STAGE_5_PROBLEMS,
    },
    {
        "id": 6,
        "title": "Số học trong đề thi HSG",
        "icon": "🔢",
        "theory": STAGE_6_THEORY,
        "weapon": STAGE_6_WEAPON,
        "problems": STAGE_6_PROBLEMS,
    },
    {
        "id": 7,
        "title": "Sắp xếp & Tìm kiếm nhị phân",
        "icon": "📈",
        "theory": STAGE_7_THEORY,
        "weapon": STAGE_7_WEAPON,
        "problems": STAGE_7_PROBLEMS,
    },
    {
        "id": 8,
        "title": "Prefix Sum, Hai con trỏ & Đệ quy có nhớ",
        "icon": "⚡",
        "theory": STAGE_8_THEORY,
        "weapon": STAGE_8_WEAPON,
        "problems": STAGE_8_PROBLEMS,
    },
]


def get_all_stages():
    """Trả về toàn bộ lộ trình học tập."""
    return STAGES


def get_stage(stage_id: int):
    """Lấy thông tin một chặng."""
    for s in STAGES:
        if s["id"] == stage_id:
            return s
    return None


def get_problem(problem_id: str):
    """Lấy thông tin một bài tập."""
    for stage in STAGES:
        for p in stage["problems"]:
            if p["id"] == problem_id:
                return p
    return None


def get_test_cases(problem_id: str):
    """Sinh 10 test cases cho bài tập."""
    gen = TEST_GENERATORS.get(problem_id)
    if gen:
        return gen()
    return []

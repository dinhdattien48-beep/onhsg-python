import os

folder = r'C:\Users\TDat\Desktop\KHKT\Onhsg\Ôn TN THPT QGia\ChuyenDe'
os.makedirs(folder, exist_ok=True)

content_exercises = r"""# BÀI TẬP THỰC HÀNH SQL
*(Viết các câu lệnh SQL vào phần "Làm Bài" bên phải và nhấn "Nộp Bài" để AI kiểm tra)*

## Cho Cơ sở dữ liệu Quản lý Học sinh gồm 2 bảng sau:

**Bảng HOC_SINH**
- `MaHS` (Khóa chính): Mã học sinh (Chuỗi)
- `HoTen`: Họ và tên học sinh (Chuỗi)
- `GioiTinh`: Giới tính ('Nam' hoặc 'Nữ')
- `NgaySinh`: Ngày sinh (Ngày)
- `MaLop`: Mã lớp (Chuỗi)

**Bảng DIEM_THI**
- `MaHS` (Khóa chính, Khóa ngoài): Mã học sinh (Chuỗi)
- `Toan`: Điểm thi Toán (Số thực)
- `Van`: Điểm thi Văn (Số thực)
- `Tin`: Điểm thi Tin học (Số thực)

---

### Yêu cầu: 
Viết 8 câu lệnh SQL (SELECT) để thực hiện các truy vấn sau. Em có thể viết 8 câu lệnh liên tiếp nhau trong bảng Code bên phải, AI Mentor sẽ đọc và chấm điểm từng câu.

**Câu 1:** Liệt kê danh sách tất cả học sinh trong bảng `HOC_SINH` gồm các thông tin: `MaHS`, `HoTen`, `MaLop`.

**Câu 2:** Liệt kê danh sách các nữ sinh (GioiTinh = 'Nữ') thuộc lớp '12A1'.

**Câu 3:** Hiển thị `MaHS`, `HoTen` và điểm `Tin` của những học sinh có điểm Tin học lớn hơn hoặc bằng 8.0. (Gợi ý: Cần kết nối 2 bảng HOC_SINH và DIEM_THI).

**Câu 4:** Tính điểm trung bình môn Toán của toàn bộ học sinh trong bảng `DIEM_THI`.

**Câu 5:** Liệt kê danh sách `MaHS`, `HoTen` của những học sinh có họ là 'Nguyễn' (Gợi ý: Dùng toán tử LIKE).

**Câu 6:** Sắp xếp danh sách học sinh theo `NgaySinh` giảm dần (Học sinh nhỏ tuổi nhất lên đầu).

**Câu 7:** Thống kê số lượng học sinh của từng lớp. Kết quả gồm: `MaLop`, `SoLuong`.

**Câu 8:** Tìm những lớp có số lượng học sinh lớn hơn 40. (Gợi ý: Dùng GROUP BY kết hợp với HAVING).
"""

with open(os.path.join(folder, '3_CoSoDuLieu_Exercises.md'), 'w', encoding='utf-8') as f:
    f.write(content_exercises)

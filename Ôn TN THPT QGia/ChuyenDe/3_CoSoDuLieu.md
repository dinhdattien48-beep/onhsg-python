# CHUYÊN ĐỀ 3: CƠ SỞ DỮ LIỆU (CSDL) VÀ SQL
*(Cập nhật theo định hướng đề thi THPT QG 2025)*

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) cốt lõi phải nhớ.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: "Bẫy" đánh lừa trong các câu hỏi trắc nghiệm khách quan & Đúng/Sai.

---

## 1. KHÁI NIỆM HỆ QUẢN TRỊ CSDL VÀ KIẾN TRÚC
1. **<span style="color: blue; text-decoration: underline;">Cơ sở dữ liệu (Database)</span>**: Tập hợp dữ liệu có cấu trúc, được lưu trữ trên máy tính.
2. **<span style="color: blue; text-decoration: underline;">Hệ quản trị CSDL (DBMS - Database Management System)</span>**: Phần mềm cung cấp môi trường tạo lập, cập nhật và khai thác dữ liệu (VD: MySQL, SQL Server, Oracle, MS Access).
3. **<span style="color: blue; text-decoration: underline;">Hệ CSDL (Database System)</span>**: Bao gồm CSDL (Dữ liệu) + Hệ quản trị CSDL (Phần mềm) + Máy tính/Phần cứng.

⚠️ **BẪY THI TRẮC NGHIỆM:**
- "<span style="color: red; text-decoration: underline;">Hệ quản trị CSDL là tên gọi khác của Cơ sở dữ liệu</span>". -> **SAI**. Một cái là **phần mềm công cụ** (DBMS), một cái là **chứa dữ liệu** (Database). Chúng hoàn toàn khác nhau. Giống như Excel (phần mềm) và File .xlsx (dữ liệu).

---

## 2. MÔ HÌNH DỮ LIỆU QUAN HỆ (RELATIONAL MODEL)
Đây là mô hình phổ biến nhất, tổ chức dữ liệu dưới dạng các <span style="color: blue; text-decoration: underline;">Bảng (Table)</span>. Thuật ngữ hàn lâm:
- **Quan hệ (Relation)** = Bảng (Table)
- **Thuộc tính (Attribute)** = Cột (Column / Field)
- **Bản ghi / Bộ (Tuple)** = Hàng (Row / Record)

### Các ràng buộc quan trọng:
1. **<span style="color: blue; text-decoration: underline;">Khóa chính (Primary Key)</span>**:
   - Dùng để phân biệt các hàng với nhau một cách duy nhất (VD: Số CMND, Mã học sinh).
   - <span style="color: blue; text-decoration: underline;">Quy tắc cốt lõi</span>: Không được để trống (NOT NULL) và không được trùng lặp (UNIQUE).
2. **<span style="color: blue; text-decoration: underline;">Khóa ngoài (Foreign Key)</span>**:
   - Thuộc tính của một bảng, nhưng tham chiếu (trỏ) tới Khóa chính của một bảng khác. Dùng để tạo liên kết (Relationship) giữa 2 bảng.
   - ⚠️ **BẪY LIÊN KẾT:** "<span style="color: red; text-decoration: underline;">Khóa ngoài bắt buộc phải có giá trị khác nhau ở mỗi hàng</span>". -> **SAI**. Chỉ Khóa chính mới cấm trùng. Khóa ngoài hoàn toàn có thể trùng lặp (Ví dụ: Nhiều học sinh chung một 'Mã Lớp' trong bảng Học sinh).

### Đặc trưng của Bảng trong CSDL Quan hệ:
- Mỗi ô chỉ chứa một giá trị nguyên tố (không chứa một danh sách hay mảng).
- ⚠️ **BẪY CỰC HAY:** "<span style="color: red; text-decoration: underline;">Nếu thay đổi thứ tự các hàng hoặc thứ tự các cột trong bảng thì ý nghĩa dữ liệu bị sai lệch</span>". -> **SAI HOÀN TOÀN**. Trong CSDL Quan hệ, thứ tự các cột và thứ tự các hàng là <span style="color: red; text-decoration: underline;">không quan trọng</span>. Đảo cột hay đảo dòng thoải mái.
- <span style="color: red; text-decoration: underline;">Không được có hai hàng (bản ghi) giống hệt nhau ở mọi cột</span>.

---

## 3. NGÔN NGỮ TRUY VẤN SQL (CẤU TRÚC SELECT)
Học sinh cần nắm rõ cú pháp và ý nghĩa của các mệnh đề trong khối lệnh `SELECT`.

**Cú pháp tổng quát:**
```sql
SELECT <cột>
FROM <bảng>
JOIN <bảng khác> ON <điều kiện nối>
WHERE <điều kiện lọc>
GROUP BY <cột gom nhóm>
HAVING <điều kiện lọc sau khi gom nhóm>
ORDER BY <cột sắp xếp>
```

1. **<span style="color: blue; text-decoration: underline;">WHERE vs HAVING</span>**:
   - ⚠️ **BẪY KINH ĐIỂN CỦA ĐỀ THI:** Đề bài yêu cầu: "Liệt kê các lớp có số lượng học sinh > 40". Nếu học sinh dùng `WHERE COUNT(MaHS) > 40` là **SAI**.
   - <span style="color: red; text-decoration: underline;">WHERE</span>: Dùng để lọc các bản ghi (hàng) riêng lẻ <span style="color: red; text-decoration: underline;">trước khi gom nhóm</span>. Không được chứa hàm tổng hợp (`SUM, COUNT, AVG`).
   - <span style="color: red; text-decoration: underline;">HAVING</span>: Dùng để lọc dữ liệu <span style="color: red; text-decoration: underline;">sau khi đã GROUP BY</span>. Chỉ dùng kèm với hàm tổng hợp.

2. **<span style="color: blue; text-decoration: underline;">INNER JOIN (Phép nối nội)</span>**:
   - Kết hợp các hàng từ 2 bảng dựa trên cột chung (thường là Khóa chính - Khóa ngoài).
   - Nếu hàng ở bảng A không có giá trị khớp ở bảng B, hàng đó sẽ bị loại khỏi kết quả.

3. **<span style="color: blue; text-decoration: underline;">Toán tử IN và LIKE</span>**:
   - `WHERE Tên LIKE 'Nguyễn%'`: Tìm tên bắt đầu bằng chữ "Nguyễn". Ký tự `%` đại diện cho một chuỗi ký tự bất kỳ.
   - `WHERE Điểm IN (8, 9, 10)`: Lấy ra những học sinh có điểm là 8, 9 hoặc 10 (tương đương với nhiều dấu OR).

# LỘ TRÌNH ÔN THI TỐT NGHIỆP THPT QUỐC GIA MÔN TIN HỌC
**(Chuyên đề: Cơ sở dữ liệu)**

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) quan trọng cần ghi nhớ.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: Các kiến thức dễ bị "Bẫy" trong đề thi, cần đặc biệt lưu ý.

---

## GIAI ĐOẠN 1: NẮM VỮNG NỀN TẢNG (Phần 1 & Phần 4)
*Mục tiêu: Hiểu rõ khái niệm, cấu trúc của hệ cơ sở dữ liệu và các thành phần cốt lõi.*

**Bài 1: Tổng quan về <span style="color: blue; text-decoration: underline;">Cơ sở dữ liệu (CSDL)</span> và <span style="color: blue; text-decoration: underline;">Mô hình dữ liệu quan hệ</span>**
- Nắm vững khái niệm về <span style="color: blue; text-decoration: underline;">Bảng (table)</span>, <span style="color: blue; text-decoration: underline;">Hàng (bản ghi/tuple)</span>, <span style="color: blue; text-decoration: underline;">Cột (thuộc tính/field)</span>.
- ⚠️ **Bẫy thường gặp:** Trong mô hình quan hệ, <span style="color: red; text-decoration: underline;">thứ tự các cột</span> và <span style="color: red; text-decoration: underline;">thứ tự các hàng</span> trong bảng là <span style="color: red; text-decoration: underline;">không quan trọng</span> (có thể đảo vị trí mà không làm thay đổi ý nghĩa dữ liệu). Đặc biệt, <span style="color: red; text-decoration: underline;">không được có hai hàng giống hệt nhau</span>.

**Bài 2: <span style="color: blue; text-decoration: underline;">Hệ quản trị CSDL (DBMS)</span> và <span style="color: blue; text-decoration: underline;">Hệ CSDL</span>**
- Phân biệt các thành phần của Hệ CSDL: <span style="color: blue; text-decoration: underline;">CSDL</span>, <span style="color: blue; text-decoration: underline;">DBMS</span> và <span style="color: blue; text-decoration: underline;">Ứng dụng</span>.
- Hiểu kiến trúc <span style="color: blue; text-decoration: underline;">CSDL tập trung</span> và <span style="color: blue; text-decoration: underline;">CSDL phân tán</span>.
- ⚠️ **Bẫy thường gặp:** Phân biệt giữa Ứng dụng cục bộ và Ứng dụng toàn cục. Đề thi thường bẫy: <span style="color: red; text-decoration: underline;">Ứng dụng toàn cục</span> chỉ chạy tại 1 trạm nhưng sử dụng dữ liệu từ <span style="color: red; text-decoration: underline;">hai trạm trở lên</span> (dễ nhầm thành "chạy trên nhiều trạm").

---

## GIAI ĐOẠN 2: TRỌNG TÂM CỐT LÕI - KHÓA VÀ RÀNG BUỘC (Phần 2)
*Mục tiêu: Phân biệt rõ các loại khóa và quy tắc thao tác dữ liệu để không vi phạm ràng buộc.*

**Bài 3: Hệ thống <span style="color: blue; text-decoration: underline;">Khóa (Key)</span>**
- Học cách phân biệt <span style="color: blue; text-decoration: underline;">Khóa dự tuyển</span>, <span style="color: blue; text-decoration: underline;">Khóa chính (Primary Key)</span> và <span style="color: blue; text-decoration: underline;">Khóa ngoài (Foreign Key)</span>.
- ⚠️ **Bẫy thường gặp về Khóa chính:** Một quan hệ (bảng) chỉ có <span style="color: red; text-decoration: underline;">duy nhất một khóa chính</span>. Khóa chính có thể gồm <span style="color: red; text-decoration: underline;">một hoặc nhiều thuộc tính</span>. Đặc biệt, giá trị khóa chính <span style="color: red; text-decoration: underline;">KHÔNG ĐƯỢC trùng lặp</span> và <span style="color: red; text-decoration: underline;">KHÔNG ĐƯỢC nhận giá trị NULL</span>.
- ⚠️ **Bẫy thường gặp về Khóa ngoài:** Ngược lại với khóa chính, Khóa ngoài <span style="color: red; text-decoration: underline;">có thể nhận giá trị NULL</span> và <span style="color: red; text-decoration: underline;">không duy nhất</span> (nhiều bản ghi có thể có cùng giá trị khóa ngoài).

**Bài 4: <span style="color: blue; text-decoration: underline;">Ràng buộc toàn vẹn</span>**
- Nắm vững <span style="color: blue; text-decoration: underline;">Ràng buộc khóa</span> và <span style="color: blue; text-decoration: underline;">Ràng buộc tham chiếu</span> (Khóa ngoài).
- ⚠️ **Bẫy thường gặp:** Giá trị của khóa ngoài ở bảng con <span style="color: red; text-decoration: underline;">bắt buộc phải tồn tại</span> trong trường khóa chính của bảng cha. 
- ⚠️ **Bẫy thao tác:** Khi <span style="color: red; text-decoration: underline;">sửa/xóa ở bảng cha</span> hoặc <span style="color: red; text-decoration: underline;">thêm/sửa ở bảng con</span>, hệ thống mới cần <span style="color: red; text-decoration: underline;">kiểm tra ràng buộc tham chiếu</span>. (Đề hay lừa là "xóa ở bảng con" thì không cần kiểm tra cha).

---

## GIAI ĐOẠN 3: THỰC HÀNH VÀ TRUY VẤN SQL (Phần 3)
*Mục tiêu: Nắm vững cú pháp truy vấn, các hàm và phân loại câu lệnh SQL.*

**Bài 5: Phân loại câu lệnh <span style="color: blue; text-decoration: underline;">SQL</span>**
- Thuộc nhóm các lệnh: <span style="color: blue; text-decoration: underline;">DQL (SELECT)</span>, <span style="color: blue; text-decoration: underline;">DML (INSERT, UPDATE, DELETE)</span>, <span style="color: blue; text-decoration: underline;">DDL (CREATE, ALTER, DROP)</span>, <span style="color: blue; text-decoration: underline;">DCL (GRANT, REVOKE)</span>.
- ⚠️ **Bẫy thường gặp:** Rất dễ nhầm lẫn chức năng của các lệnh. Ví dụ: <span style="color: red; text-decoration: underline;">DELETE</span> là để xóa dữ liệu (DML), trong khi <span style="color: red; text-decoration: underline;">DROP TABLE</span> là xóa hẳn cấu trúc bảng (DDL).

**Bài 6: Cấu trúc <span style="color: blue; text-decoration: underline;">SELECT</span> và <span style="color: blue; text-decoration: underline;">Hàm tổng hợp</span>**
- Cú pháp chuẩn: SELECT -> FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> ORDER BY.
- ⚠️ **Bẫy thường gặp:** Phân biệt rõ <span style="color: red; text-decoration: underline;">WHERE</span> (điều kiện lọc các hàng <span style="color: red; text-decoration: underline;">trước khi gom nhóm</span>) và <span style="color: red; text-decoration: underline;">HAVING</span> (điều kiện lọc <span style="color: red; text-decoration: underline;">sau khi đã gom nhóm</span>). 
- Các phép toán như IN, BETWEEN, và <span style="color: blue; text-decoration: underline;">Phép nối bảng (INNER JOIN)</span> phải ghép qua cột liên kết (thường là Khóa chính - Khóa ngoài).

---

## GIAI ĐOẠN 4: VẬN HÀNH, BẢO MẬT & AN TOÀN (Phần 5)
*Mục tiêu: Tránh mất điểm ở các câu hỏi lý thuyết khái niệm cuối.*

**Bài 7: <span style="color: blue; text-decoration: underline;">Bảo mật CSDL (Security)</span> và <span style="color: blue; text-decoration: underline;">An toàn CSDL (Safety)</span>**
- Hiểu các kỹ thuật: <span style="color: blue; text-decoration: underline;">Xác thực (Authentication)</span>, <span style="color: blue; text-decoration: underline;">Phân quyền (Authorization)</span>, <span style="color: blue; text-decoration: underline;">Mã hóa</span>, <span style="color: blue; text-decoration: underline;">Sao lưu và phục hồi</span>.
- ⚠️ **Bẫy cực kỳ phổ biến:** Đề thi rất hay tráo đổi hai định nghĩa này:
  - <span style="color: red; text-decoration: underline;">Bảo mật (Security)</span>: Là chống lại các mối đe dọa chủ ý như <span style="color: red; text-decoration: underline;">hacker, lộ lọt thông tin, thay đổi trái phép</span>.
  - <span style="color: red; text-decoration: underline;">An toàn (Safety)</span>: Là bảo vệ dữ liệu khỏi sự cố <span style="color: red; text-decoration: underline;">khách quan</span> như <span style="color: red; text-decoration: underline;">hỏng ổ cứng, mất điện, hỏa hoạn</span> (Khắc phục bằng sao lưu).

---
*Chúc bạn ôn tập hiệu quả và đạt điểm tuyệt đối môn Tin Học!*

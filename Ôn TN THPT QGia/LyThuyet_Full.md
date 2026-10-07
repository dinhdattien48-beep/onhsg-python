# LÝ THUYẾT TRỌNG TÂM ÔN THI TỐT NGHIỆP THPT QUỐC GIA (TIN HỌC)
*(Cập nhật theo cấu trúc đề thi GDPT 2018 - áp dụng từ 2025)*

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) quan trọng.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: "Bẫy" trong đề thi, những chỗ học sinh dễ sai.

---

## CHUYÊN ĐỀ 1: MẠNG MÁY TÍNH VÀ INTERNET
*Mục tiêu: Nắm vững cấu trúc mạng, các thiết bị và giao thức cơ bản.*

**1. Khái niệm và phân loại mạng**
- <span style="color: blue; text-decoration: underline;">Mạng LAN (Local Area Network)</span>: Mạng cục bộ, kết nối trong phạm vi nhỏ (phòng máy, trường học).
- <span style="color: blue; text-decoration: underline;">Mạng WAN (Wide Area Network)</span>: Mạng diện rộng, kết nối các vùng lãnh thổ. <span style="color: blue; text-decoration: underline;">Internet</span> là mạng WAN lớn nhất.
- ⚠️ **Bẫy thường gặp:** Đề hay lừa rằng <span style="color: red; text-decoration: underline;">Mạng LAN có tốc độ truyền dữ liệu thấp hơn WAN</span>. Thực tế, mạng LAN thường có <span style="color: red; text-decoration: underline;">tốc độ cao hơn</span> mạng WAN rất nhiều vì khoảng cách ngắn và thiết bị chuyên dụng.

**2. Các thiết bị mạng cơ bản**
- <span style="color: blue; text-decoration: underline;">Switch (Bộ chuyển mạch)</span>: Kết nối các máy tính trong cùng một mạng LAN. Gửi dữ liệu đúng tới máy đích.
- <span style="color: blue; text-decoration: underline;">Router (Bộ định tuyến)</span>: Kết nối **các mạng LAN khác nhau** hoặc kết nối LAN với Internet.
- ⚠️ **Bẫy:** Đừng nhầm lẫn giữa Switch và Router. <span style="color: red; text-decoration: underline;">Switch chỉ hoạt động nội bộ</span> trong 1 mạng, còn <span style="color: red; text-decoration: underline;">Router làm nhiệm vụ dẫn đường (routing)</span> ra ngoài Internet.
- <span style="color: blue; text-decoration: underline;">Access Point (AP)</span>: Trạm phát sóng Wifi.

**3. Giao thức mạng**
- <span style="color: blue; text-decoration: underline;">TCP/IP</span>: Bộ giao thức nền tảng của Internet. <span style="color: blue; text-decoration: underline;">IP</span> xác định địa chỉ, <span style="color: blue; text-decoration: underline;">TCP</span> đảm bảo truyền dữ liệu không bị mất.
- ⚠️ **Bẫy:** <span style="color: red; text-decoration: underline;">Địa chỉ IP (IPv4)</span> gồm 4 cụm số cách nhau bởi dấu chấm, mỗi cụm <span style="color: red; text-decoration: underline;">chỉ có giá trị từ 0 đến 255</span>. Ví dụ `192.168.1.300` là một địa chỉ IP **sai**.

---

## CHUYÊN ĐỀ 2: TRÍ TUỆ NHÂN TẠO (AI)
*Mục tiêu: Hiểu bản chất AI và các hệ chuyên gia.*

**1. Khái niệm cơ bản**
- <span style="color: blue; text-decoration: underline;">Trí tuệ nhân tạo (AI)</span>: Là ngành khoa học máy tính nhằm tạo ra máy móc có khả năng mô phỏng trí tuệ con người (học tập, lập luận, hiểu ngôn ngữ).
- <span style="color: blue; text-decoration: underline;">Học máy (Machine Learning)</span>: Là một nhánh của AI, cho phép máy tính **tự học** từ dữ liệu thay vì được lập trình tĩnh.

**2. Các ứng dụng thực tế**
- <span style="color: blue; text-decoration: underline;">Thị giác máy tính (Computer Vision)</span>: Nhận diện khuôn mặt, chẩn đoán ảnh y tế.
- <span style="color: blue; text-decoration: underline;">Xử lý ngôn ngữ tự nhiên (NLP)</span>: ChatGPT, Google Translate.
- ⚠️ **Bẫy trắc nghiệm Đúng/Sai:** Đề thi phần II thường cho mệnh đề: "<span style="color: red; text-decoration: underline;">AI có thể suy nghĩ và có cảm xúc giống hệt con người</span>". Mệnh đề này là **SAI**. AI hiện tại (AI hẹp) chỉ <span style="color: red; text-decoration: underline;">mô phỏng</span> lại hành vi dựa trên xác suất toán học và dữ liệu, hoàn toàn **không có ý thức hay cảm xúc**.

---

## CHUYÊN ĐỀ 3: CƠ SỞ DỮ LIỆU (CSDL) VÀ SQL
*Mục tiêu: Nắm vững bảng, khóa, quan hệ và truy vấn (Nội dung ăn điểm nhất).*

**1. Khái niệm và Kiến trúc**
- Nắm vững khái niệm về <span style="color: blue; text-decoration: underline;">Bảng (table)</span>, <span style="color: blue; text-decoration: underline;">Hàng (bản ghi/record)</span>, <span style="color: blue; text-decoration: underline;">Cột (thuộc tính/field)</span>.
- ⚠️ **Bẫy:** Trong mô hình quan hệ, <span style="color: red; text-decoration: underline;">thứ tự các cột và hàng là không quan trọng</span>. Đặc biệt, <span style="color: red; text-decoration: underline;">không được có hai hàng (bản ghi) giống hệt nhau</span>.
- Cấu trúc hệ CSDL gồm: <span style="color: blue; text-decoration: underline;">CSDL</span>, <span style="color: blue; text-decoration: underline;">Hệ quản trị CSDL (DBMS)</span>, và <span style="color: blue; text-decoration: underline;">Ứng dụng</span>.

**2. Ràng buộc toàn vẹn và Khóa**
- <span style="color: blue; text-decoration: underline;">Khóa chính (Primary Key)</span>: Một bảng chỉ có **duy nhất một khóa chính** (có thể gồm nhiều thuộc tính).
- ⚠️ **Bẫy:** Giá trị khóa chính <span style="color: red; text-decoration: underline;">KHÔNG ĐƯỢC trùng lặp</span> và <span style="color: red; text-decoration: underline;">KHÔNG ĐƯỢC để trống (NULL)</span>.
- <span style="color: blue; text-decoration: underline;">Khóa ngoài (Foreign Key)</span>: Dùng để liên kết các bảng.
- ⚠️ **Bẫy thao tác:** Khi thêm/sửa bản ghi ở bảng con, khóa ngoài của nó <span style="color: red; text-decoration: underline;">bắt buộc phải tồn tại trong khóa chính bảng cha</span>. Khóa ngoài <span style="color: red; text-decoration: underline;">ĐƯỢC PHÉP chứa giá trị NULL</span> hoặc trùng lặp.

**3. Ngôn ngữ SQL cơ bản**
- Các lệnh thao tác: <span style="color: blue; text-decoration: underline;">SELECT</span> (truy vấn), <span style="color: blue; text-decoration: underline;">INSERT</span> (thêm), <span style="color: blue; text-decoration: underline;">UPDATE</span> (sửa), <span style="color: blue; text-decoration: underline;">DELETE</span> (xóa dữ liệu).
- ⚠️ **Bẫy phân loại:** Đề hay lừa giữa việc xóa dữ liệu (DML) và xóa bảng (DDL). <span style="color: red; text-decoration: underline;">DELETE</span> chỉ xóa các hàng trong bảng, còn <span style="color: red; text-decoration: underline;">DROP TABLE</span> xóa hoàn toàn cấu trúc bảng khỏi đĩa.
- Cú pháp chuẩn của truy vấn: SELECT -> FROM -> WHERE -> GROUP BY -> HAVING.
- ⚠️ **Bẫy điều kiện:** Phân biệt rõ <span style="color: red; text-decoration: underline;">WHERE</span> (điều kiện lọc các hàng **trước** khi gom nhóm) và <span style="color: red; text-decoration: underline;">HAVING</span> (điều kiện lọc **sau** khi đã dùng GROUP BY). Đề hay cho HAVING nhưng lại áp dụng cho trường không nằm trong hàm tổng hợp.

---

## CHUYÊN ĐỀ 4: TẠO TRANG WEB (HTML & CSS)
*Mục tiêu: Hiểu cấu trúc thẻ HTML và định dạng CSS.*

**1. Cấu trúc HTML (HyperText Markup Language)**
- Trang web được hình thành bởi các <span style="color: blue; text-decoration: underline;">Thẻ (Tag)</span>. Gồm thẻ mở `<tag>` và thẻ đóng `</tag>`.
- Các thẻ cơ bản: `<html>`, `<head>`, `<body>`, `<h1>` đến `<h6>`, `<p>` (đoạn văn), `<a>` (liên kết), `<img>` (hình ảnh).
- ⚠️ **Bẫy thuộc tính:** Thẻ `<a>` bắt buộc phải có thuộc tính <span style="color: red; text-decoration: underline;">href="..."</span> để tạo link. Thẻ `<img>` bắt buộc phải có <span style="color: red; text-decoration: underline;">src="..."</span> để trỏ tới file ảnh. Đề thường cố tình viết thiếu hai thuộc tính này.

**2. Định dạng CSS (Cascading Style Sheets)**
- Bộ chọn (Selector):
  - <span style="color: blue; text-decoration: underline;">#id</span>: Chọn một phần tử duy nhất có `id` tương ứng (Ví dụ: `#header`).
  - <span style="color: blue; text-decoration: underline;">.class</span>: Chọn nhiều phần tử có chung `class` (Ví dụ: `.text-red`).
- ⚠️ **Bẫy CSS:** Đề bài thường hỏi cú pháp liên kết file CSS ngoài. Cú pháp ĐÚNG là <span style="color: red; text-decoration: underline;">`<link rel="stylesheet" href="style.css">`</span> đặt trong thẻ `<head>`. Rất nhiều học sinh chọn nhầm thành thẻ `<style src="style.css">` (Sai cú pháp hoàn toàn).

---

## CHUYÊN ĐỀ 5: BẢO MẬT VÀ AN TOÀN THÔNG TIN
*Mục tiêu: Phân biệt các rủi ro mạng và khái niệm an toàn/bảo mật.*

- <span style="color: blue; text-decoration: underline;">Malware (Mã độc)</span>: Bao gồm Virus, Trojan, Ransomware (mã độc tống tiền).
- ⚠️ **Bẫy khái niệm:** Đề thi rất hay tráo đổi hai định nghĩa sau:
  - <span style="color: red; text-decoration: underline;">Bảo mật (Security)</span>: Là chống lại các mối đe dọa chủ ý như <span style="color: red; text-decoration: underline;">hacker, lộ lọt thông tin, thay đổi trái phép</span>. Giải pháp là xác thực, phân quyền, mật khẩu, mã hóa.
  - <span style="color: red; text-decoration: underline;">An toàn (Safety)</span>: Là bảo vệ dữ liệu khỏi sự cố <span style="color: red; text-decoration: underline;">khách quan</span> như <span style="color: red; text-decoration: underline;">hỏng ổ cứng, mất điện, hỏa hoạn</span>. Giải pháp chính là **Sao lưu (Backup)** và phục hồi.
  *(Ví dụ Bẫy: "Anh A bị hỏng ổ cứng do rơi laptop, anh A bị vi phạm bảo mật" -> SAI, đây là vấn đề An toàn).*

---
*Lưu ý: Phần thi trắc nghiệm Đúng/Sai (Phần II) chiếm 40% điểm. Em phải đọc rất kỹ từng chữ trong câu mệnh đề để tránh các từ "chỉ có", "luôn luôn", "tất cả" - thường là dấu hiệu của mệnh đề Sai.*

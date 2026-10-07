# CHUYÊN ĐỀ 4: HTML VÀ CSS CĂN BẢN
*(Cập nhật theo định hướng đề thi THPT QG 2025)*

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) cốt lõi phải nhớ.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: "Bẫy" đánh lừa trong các câu hỏi trắc nghiệm khách quan & Đúng/Sai.

---

## 1. TỔNG QUAN VỀ HTML (NGÔN NGỮ ĐÁNH DẤU SIÊU VĂN BẢN)
HTML (HyperText Markup Language) <span style="color: blue; text-decoration: underline;">không phải là ngôn ngữ lập trình</span>, nó là ngôn ngữ đánh dấu để tạo ra cấu trúc (bộ xương) cho trang web.

### Cấu trúc cơ bản của một trang HTML5:
```html
<!DOCTYPE html>
<html>
    <head>
        <!-- Chứa siêu dữ liệu, tiêu đề, liên kết CSS. Phần này không hiển thị lên màn hình người dùng -->
        <title>Tiêu đề trang</title>
        <meta charset="utf-8">
    </head>
    <body>
        <!-- Chứa toàn bộ nội dung mà người dùng sẽ nhìn thấy -->
    </body>
</html>
```
⚠️ **BẪY TRẮC NGHIỆM:**
- "<span style="color: red; text-decoration: underline;">Nội dung nằm trong cặp thẻ `<head>` sẽ được hiển thị ở phần đầu của trang web trên màn hình người dùng</span>". -> **SAI**. Những gì hiển thị trên màn hình phải nằm trong thẻ `<body>`. Thẻ `<head>` chỉ chứa thông tin kỹ thuật cho trình duyệt và công cụ tìm kiếm.

### Các thẻ HTML trọng tâm:
1. **Các thẻ tiêu đề (`<h1>` đến `<h6>`)**: Thẻ `<h1>` to nhất, `<h6>` nhỏ nhất.
2. **Thẻ liên kết siêu văn bản (`<a>`)**:
   - Thuộc tính bắt buộc: `href` (để chỉ định URL đích).
   - ⚠️ **Bẫy thi:** Dùng sai thuộc tính (VD: `<a link="google.com">` hoặc `<a src="google.com">` là **SAI**, phải là `<a href="...">`).
3. **Thẻ hình ảnh (`<img>`)**:
   - Thẻ rỗng (không có thẻ đóng).
   - Hai thuộc tính cực kỳ quan trọng: `src` (đường dẫn ảnh) và `alt` (văn bản thay thế khi ảnh bị lỗi).
   - ⚠️ **Bẫy thi:** "<span style="color: red; text-decoration: underline;">Thuộc tính alt không bắt buộc, bỏ đi web vẫn chạy mượt nên không có tác dụng gì</span>". -> **SAI**. `alt` rất quan trọng cho SEO (Google đọc hiểu ảnh) và cho người khiếm thị dùng phần mềm đọc màn hình.
4. **Tạo danh sách**:
   - `<ul>` (Unordered List): Danh sách có dấu chấm tròn (không thứ tự).
   - `<ol>` (Ordered List): Danh sách có đánh số 1, 2, 3 (có thứ tự).
   - Phần tử con bắt buộc của cả hai là `<li>` (List item).

---

## 2. TỔNG QUAN VỀ CSS (CASCADING STYLE SHEETS)
CSS đóng vai trò <span style="color: blue; text-decoration: underline;">trang trí và bố cục</span> (màu sắc, kích thước, font chữ) cho trang web. HTML là "bộ xương", CSS là "lớp da và quần áo".

### Cú pháp CSS:
```css
Bộ_chọn {
    thuộc_tính: giá_trị;
}
/* Ví dụ: */
h1 {
    color: red;
    font-size: 20px;
}
```

### 3 cách chèn CSS vào HTML:
1. **<span style="color: blue; text-decoration: underline;">Inline CSS (Nội tuyến)</span>**: Viết trực tiếp vào thuộc tính `style` của thẻ HTML. (VD: `<p style="color: red;">`). Khó bảo trì nhất.
2. **<span style="color: blue; text-decoration: underline;">Internal CSS (Bên trong)</span>**: Viết trong cặp thẻ `<style>` đặt bên trong thẻ `<head>` của file HTML.
3. **<span style="color: blue; text-decoration: underline;">External CSS (Bên ngoài)</span>**: Viết CSS ra một file `.css` riêng biệt rồi nhúng vào HTML bằng thẻ `<link rel="stylesheet" href="style.css">`. (Khuyên dùng nhất).

⚠️ **BẪY ƯU TIÊN CSS (Độ ưu tiên / Specificity):**
- Đề thi thường hỏi: "Nếu cùng tác động đổi màu chữ vào 1 thẻ `<p>` bằng cả 3 cách trên, màu nào sẽ được áp dụng?".
- **Luật ưu tiên**: <span style="color: red; text-decoration: underline;">Inline CSS (Gần thẻ nhất) > Internal CSS > External CSS</span>.
- Ngoài ra: Bộ chọn ID (`#id`) mạnh hơn Bộ chọn Lớp (`.class`), mạnh hơn Bộ chọn Thẻ (`p, h1`).

### CSS Box Model (Mô hình hộp):
Đây là kiến thức cực kỳ quan trọng về bố cục phần tử. Mọi thẻ HTML đều là một cái hộp vuông vức gồm 4 lớp từ trong ra ngoài:
1. **Content**: Nội dung chữ hoặc ảnh cốt lõi.
2. **Padding (Vùng đệm)**: Khoảng trống <span style="color: blue; text-decoration: underline;">bên trong</span> hộp (từ viền đẩy vào Content). Màu nền sẽ lan vào phần Padding.
3. **Border (Viền)**: Đường viền bao quanh hộp.
4. **Margin (Lề)**: Khoảng trống <span style="color: blue; text-decoration: underline;">bên ngoài</span> hộp (Đẩy các hộp khác ra xa).

⚠️ **BẪY BOX MODEL:**
- "<span style="color: red; text-decoration: underline;">Margin và Padding là giống nhau, đều tạo khoảng trống</span>". -> **SAI**. Margin tạo khoảng cách bên ngoài viền (không có màu nền), Padding tạo khoảng cách bên trong viền (có màu nền).

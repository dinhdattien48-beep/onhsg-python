import os

folder = r'C:\Users\TDat\Desktop\KHKT\Onhsg\Ôn TN THPT QGia\ChuyenDe'
os.makedirs(folder, exist_ok=True)

content_4 = r"""# CHUYÊN ĐỀ 4: HTML VÀ CSS CĂN BẢN (NÂNG CAO & THỰC HÀNH)
*(Cập nhật theo định hướng đề thi THPT QG 2025)*

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) cốt lõi phải nhớ.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: "Bẫy" đánh lừa trong các câu hỏi trắc nghiệm khách quan & Đúng/Sai.

---

## 1. TỔNG QUAN VỀ HTML (NGÔN NGỮ ĐÁNH DẤU SIÊU VĂN BẢN)
HTML (HyperText Markup Language) <span style="color: blue; text-decoration: underline;">không phải là ngôn ngữ lập trình</span>, nó là ngôn ngữ đánh dấu để tạo ra cấu trúc (bộ xương) cho trang web. Các tài liệu HTML được mô tả bởi các thẻ (tags).

### Cấu trúc chuẩn của một trang HTML5:
Mọi trang web đều phải tuân theo khung xương cơ bản sau đây. Học sinh cần ghi nhớ kỹ vị trí của từng thẻ.

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Tiêu đề trang web</title>
        <style>
            /* Nơi viết CSS nội tuyến (Internal CSS) */
        </style>
    </head>
    <body>
        <h1>Trang web đầu tiên của tôi</h1>
        <p>Chào mừng bạn đến với thế giới lập trình web!</p>
    </body>
</html>
```

⚠️ **BẪY TRẮC NGHIỆM:**
- "<span style="color: red; text-decoration: underline;">Nội dung nằm trong cặp thẻ `<head>` sẽ được hiển thị ở phần đầu của trang web trên màn hình người dùng</span>". -> **SAI**. Những gì hiển thị trên màn hình phải nằm trong thẻ `<body>`. Thẻ `<head>` chỉ chứa thông tin kỹ thuật (meta) cho trình duyệt và công cụ tìm kiếm (Google).
- "<span style="color: red; text-decoration: underline;">Thẻ `<!DOCTYPE html>` là một thẻ HTML dùng để định dạng chữ</span>". -> **SAI**. Đó là lời khai báo cho trình duyệt biết đây là tài liệu HTML phiên bản 5. Nó không phải là thẻ HTML và không có thẻ đóng.

---

## 2. CÁC THẺ HTML TRỌNG TÂM TRONG ĐỀ THI

1. **Các thẻ định dạng văn bản**:
   - `<h1>` đến `<h6>`: Các thẻ tiêu đề. `<h1>` có kích thước chữ to nhất, `<h6>` nhỏ nhất.
   - `<p>` (Paragraph): Thẻ tạo đoạn văn bản. Trình duyệt tự động thêm khoảng trắng trước và sau đoạn văn.
   - `<b>` và `<strong>`: Đều làm in đậm chữ, nhưng `<strong>` nhấn mạnh về mặt <span style="color: blue; text-decoration: underline;">ngữ nghĩa</span> (quan trọng đối với SEO và trình đọc màn hình).
   - `<i>` và `<em>`: Đều làm in nghiêng chữ, tương tự, `<em>` (emphasis) mang ý nghĩa nhấn mạnh.

2. **Thẻ liên kết siêu văn bản (`<a>`)**:
   - Dùng để chuyển hướng (link) sang trang khác.
   - Thuộc tính bắt buộc: <span style="color: blue; text-decoration: underline;">`href`</span> (chỉ định URL đích).
   - Ví dụ: `<a href="https://google.com">Đến Google</a>`
   - ⚠️ **Bẫy thi:** Đề thường cố tình viết sai thuộc tính như `<a link="google.com">` hoặc `<a src="google.com">`. Đáp án phải là **`href`**.

3. **Thẻ hình ảnh (`<img>`)**:
   - Thẻ rỗng (không có thẻ đóng, tự đóng ngay trên chính nó `/>` hoặc chỉ `<img ...>`).
   - Hai thuộc tính cực kỳ quan trọng:
     + <span style="color: blue; text-decoration: underline;">`src`</span>: Đường dẫn (source) trỏ tới file ảnh.
     + <span style="color: blue; text-decoration: underline;">`alt`</span>: Văn bản thay thế (hiển thị khi ảnh bị lỗi không tải được).
   - Ví dụ: `<img src="dog.jpg" alt="Hình một chú chó">`
   - ⚠️ **Bẫy thi:** "<span style="color: red; text-decoration: underline;">Thuộc tính alt không bắt buộc, bỏ đi web vẫn chạy mượt nên không có tác dụng gì</span>". -> **SAI**. `alt` rất quan trọng cho SEO và hỗ trợ người khiếm thị.

4. **Tạo danh sách**:
   - `<ul>` (Unordered List): Danh sách <span style="color: blue; text-decoration: underline;">không thứ tự</span> (có dấu chấm tròn ở đầu).
   - `<ol>` (Ordered List): Danh sách <span style="color: blue; text-decoration: underline;">có thứ tự</span> (đánh số 1, 2, 3... hoặc A, B, C...).
   - Phần tử con bắt buộc bên trong cả hai loại danh sách là thẻ `<li>` (List item).

---

## 3. TỔNG QUAN VỀ CSS (CASCADING STYLE SHEETS)
CSS đóng vai trò <span style="color: blue; text-decoration: underline;">trang trí và bố cục</span> (màu sắc, kích thước, font chữ) cho trang web. Nếu HTML là "bộ xương" thì CSS là "lớp da, quần áo, mỹ phẩm".

### Cú pháp CSS:
```css
Bộ_chọn {
    thuộc_tính: giá_trị;
}
/* Ví dụ: */
h1 {
    color: blue;
    text-align: center;
}
```

### 3 cách chèn CSS vào HTML:
1. **<span style="color: blue; text-decoration: underline;">Inline CSS (Nội tuyến)</span>**: Viết trực tiếp vào thuộc tính `style` của thẻ HTML.
   - VD: `<p style="color: red;">Chữ đỏ</p>`
   - Nhược điểm: Rất khó quản lý và bảo trì nếu trang web lớn.
2. **<span style="color: blue; text-decoration: underline;">Internal CSS (Bên trong)</span>**: Viết trong cặp thẻ `<style>` đặt bên trong thẻ `<head>` của file HTML.
3. **<span style="color: blue; text-decoration: underline;">External CSS (Bên ngoài)</span>**: Viết CSS ra một file `.css` riêng biệt (ví dụ: `style.css`) rồi nhúng vào HTML bằng thẻ `<link rel="stylesheet" href="style.css">`. Đây là cách chuẩn nhất.

⚠️ **BẪY ƯU TIÊN CSS (Cascading Rules):**
- Đề thi thường đưa ra tình huống: "Thẻ `<p>` bị tác động đổi màu bởi cả 3 cách: File ngoài quy định màu xanh, thẻ `<style>` quy định màu vàng, nhưng tại thẻ HTML lại ghi `<p style="color: red;">`. Hỏi chữ sẽ có màu gì?"
- **Luật ưu tiên cốt lõi**: <span style="color: red; text-decoration: underline;">Inline CSS (Gần thẻ nhất) mạnh nhất > Internal CSS > External CSS</span>.
- Do đó, đáp án luôn là màu cấu hình trong Inline CSS (Màu đỏ).

### CSS Box Model (Mô hình hộp):
Mọi phần tử HTML đều là một cái hộp vuông vức gồm 4 thành phần (tính từ trong ra ngoài):
1. **Content**: Nội dung chữ hoặc ảnh cốt lõi.
2. **Padding (Vùng đệm)**: Khoảng trống <span style="color: blue; text-decoration: underline;">bên trong</span> hộp (từ viền đẩy vào Content). Màu nền sẽ phủ lên toàn bộ vùng Padding.
3. **Border (Viền)**: Đường viền bao quanh hộp.
4. **Margin (Lề)**: Khoảng trống <span style="color: blue; text-decoration: underline;">bên ngoài</span> hộp (dùng để đẩy các hộp khác ra xa).

⚠️ **BẪY BOX MODEL:**
- "<span style="color: red; text-decoration: underline;">Margin và Padding hoàn toàn giống nhau, đều có chức năng tạo khoảng trống</span>". -> **SAI**. Dù đều tạo khoảng cách, nhưng Margin tạo ở bên ngoài viền (trong suốt, không hiển thị màu nền), còn Padding tạo ở bên trong viền (có hiển thị màu nền). Nhầm lẫn 2 cái này sẽ làm lệch tung thiết kế giao diện!

---

## 4. HƯỚNG DẪN THỰC HÀNH TẠO MỘT TRANG WEB HOÀN CHỈNH
Mục này cung cấp mẫu code để bạn copy/paste vào phần Code Editor bên phải và chạy thử để hiểu cách HTML và CSS kết hợp với nhau. Hãy thay đổi các giá trị (VD: `color: green;`) để xem hiệu ứng.

### Bài toán: Viết một trang web giới thiệu Bản thân
- Yêu cầu: Có tiêu đề, hình ảnh chân dung, một danh sách các sở thích và một nút liên kết. Giao diện được căn giữa.

**Bước 1: Viết bộ khung HTML và liên kết CSS**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Trang cá nhân của tôi</title>
    <style>
        /* CSS sẽ được viết ở đây */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            text-align: center; /* Căn giữa toàn bộ chữ */
        }
        .container {
            width: 80%;
            margin: auto; /* Kỹ thuật căn giữa một cái hộp lớn */
            background-color: white;
            padding: 20px;
            border-radius: 10px; /* Bo góc */
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        }
        img {
            width: 150px;
            border-radius: 50%; /* Biến ảnh vuông thành ảnh tròn */
            border: 3px solid #0056b3;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #0056b3;
            color: white;
            text-decoration: none; /* Xóa gạch chân của thẻ <a> */
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Nguyễn Văn A</h1>
        <img src="https://via.placeholder.com/150" alt="Ảnh của tôi">
        <p>Chào bạn, tôi là một học sinh yêu thích lập trình và thiết kế web.</p>
        
        <h3 style="text-align: left;">Sở thích của tôi:</h3>
        <ul style="text-align: left;">
            <li>Lập trình Python và làm bài tập thuật toán</li>
            <li>Đọc sách khoa học viễn tưởng</li>
            <li>Tham gia các giải thi đấu eSports</li>
        </ul>

        <a href="https://github.com" class="btn">Ghé thăm GitHub của tôi</a>
    </div>

</body>
</html>
```

### Giải thích các kỹ thuật nâng cao thường gặp trong đề:
1. **Bộ chọn Class (`.container`, `.btn`)**: Trong CSS, dấu chấm `.` đứng đầu biểu thị cho `class`. Nếu là dấu `#` đứng đầu thì biểu thị cho `id`. Thẻ HTML nào có thuộc tính `class="btn"` sẽ nhận toàn bộ style của bộ chọn `.btn`.
2. **Kỹ thuật căn giữa khối (`margin: auto;`)**: Là bí kíp kinh điển. Khi một khối `div` được cung cấp độ rộng cụ thể (`width: 80%`), việc thêm `margin: auto;` sẽ yêu cầu trình duyệt tự động chia đều khoảng cách lề thừa ra 2 bên trái/phải, làm khối lập tức nằm giữa màn hình.
3. **Màu sắc trong CSS**: Đề thi có thể hỏi về các mã màu. `#f4f4f9` là mã màu Hệ Thập lục phân (Hex), `rgba(0,0,0,0.1)` là hệ màu đỏ-xanhlá-xanhdương kèm độ trong suốt `a` (alpha).
"""

with open(os.path.join(folder, '4_HTML_CSS.md'), 'w', encoding='utf-8') as f:
    f.write(content_4)

print("Đã cập nhật chuyên đề 4 thành công")

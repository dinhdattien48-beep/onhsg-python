import os

folder = r'C:\Users\TDat\Desktop\KHKT\Onhsg\Ôn TN THPT QGia\ChuyenDe'
os.makedirs(folder, exist_ok=True)

content_1 = r"""# CHUYÊN ĐỀ 1: MẠNG MÁY TÍNH VÀ INTERNET
*(Cập nhật theo định hướng đề thi THPT QG 2025)*

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) cốt lõi phải nhớ.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: "Bẫy" đánh lừa trong các câu hỏi trắc nghiệm khách quan & Đúng/Sai.

---

## 1. MẠNG MÁY TÍNH LÀ GÌ? PHÂN LOẠI MẠNG
Mạng máy tính là một tập hợp các thiết bị được kết nối với nhau nhằm mục đích <span style="color: blue; text-decoration: underline;">chia sẻ tài nguyên</span> (dữ liệu, máy in, phần mềm) và <span style="color: blue; text-decoration: underline;">giao tiếp</span>.

### Phân loại theo phạm vi địa lý:
1. **<span style="color: blue; text-decoration: underline;">Mạng LAN (Local Area Network)</span>**:
   - Là mạng cục bộ, kết nối trong một phạm vi nhỏ như phòng máy, tòa nhà, trường học.
   - **Đặc điểm**: Tốc độ truyền tải <span style="color: blue; text-decoration: underline;">rất cao</span>, chi phí thiết lập thấp, dễ quản trị.
   - ⚠️ **Bẫy thi:** Đề hay lừa là: "<span style="color: red; text-decoration: underline;">Mạng LAN do kết nối nhỏ nên tốc độ truyền dữ liệu thấp hơn Internet/WAN</span>". -> **SAI HOÀN TOÀN**. Do khoảng cách ngắn và thiết bị kết nối trực tiếp (cáp quang/cáp đồng nội bộ), LAN có tốc độ cao hơn mạng diện rộng rất nhiều.

2. **<span style="color: blue; text-decoration: underline;">Mạng WAN (Wide Area Network)</span>**:
   - Là mạng diện rộng, kết nối các vùng lãnh thổ, quốc gia. <span style="color: blue; text-decoration: underline;">Internet là mạng WAN lớn nhất</span>.
   - **Đặc điểm**: Tốc độ truyền tải thấp hơn LAN, độ trễ cao hơn, chi phí đắt đỏ, cấu trúc cực kỳ phức tạp.

---

## 2. CÁC THIẾT BỊ MẠNG CƠ BẢN
Thiết bị mạng đóng vai trò làm trạm trung chuyển dữ liệu. Học sinh phải phân biệt cực kỳ rõ chức năng của từng loại.

1. **<span style="color: blue; text-decoration: underline;">Switch (Bộ chuyển mạch)</span>**:
   - Thiết bị trung tâm của mạng LAN (kiến trúc hình sao).
   - <span style="color: blue; text-decoration: underline;">Chức năng</span>: Nhận gói dữ liệu từ một máy và gửi **đúng đến máy đích** thông qua bảng địa chỉ MAC. Giúp mạng không bị nghẽn (khác với Hub gửi bừa bãi cho tất cả mọi người).
   - ⚠️ **Bẫy thi:** "<span style="color: red; text-decoration: underline;">Switch có chức năng kết nối các mạng LAN khác nhau để ra Internet</span>" -> **SAI**. Switch <span style="color: red; text-decoration: underline;">chỉ hoạt động nội bộ trong 1 mạng LAN</span>, nó không biết đường ra Internet.

2. **<span style="color: blue; text-decoration: underline;">Router (Bộ định tuyến)</span>**:
   - <span style="color: blue; text-decoration: underline;">Chức năng</span>: Kết nối <span style="color: blue; text-decoration: underline;">các mạng LAN khác nhau</span> lại với nhau, hoặc kết nối một mạng LAN vào Internet.
   - ⚠️ **Bẫy thi:** Router làm nhiệm vụ <span style="color: red; text-decoration: underline;">tìm đường đi tốt nhất (routing)</span> cho gói tin qua các mạng. Đừng bao giờ nhầm lẫn chức năng này với Switch.

3. **<span style="color: blue; text-decoration: underline;">Access Point (AP - Điểm truy cập không dây)</span>**:
   - Đóng vai trò cầu nối giữa mạng có dây (LAN) và thiết bị không dây (Wi-Fi).
   - ⚠️ **Bẫy thi:** "<span style="color: red; text-decoration: underline;">Access Point có thể thay thế hoàn toàn Router để cấp phát IP ra Internet</span>" -> **SAI**. AP đơn thuần chỉ phát sóng wifi, nó vẫn cần cắm vào một Router để lấy IP và ra mạng.

---

## 3. GIAO THỨC MẠNG (PROTOCOL) VÀ ĐỊA CHỈ IP
1. **<span style="color: blue; text-decoration: underline;">Bộ giao thức TCP/IP</span>**:
   - Đây là ngôn ngữ chung của Internet. Nếu không có TCP/IP, máy tính Windows không thể hiểu máy tính Mac, điện thoại không hiểu được máy chủ web.
   - <span style="color: blue; text-decoration: underline;">IP (Internet Protocol)</span>: Phân phát gói tin đến đúng địa chỉ đích.
   - <span style="color: blue; text-decoration: underline;">TCP (Transmission Control Protocol)</span>: Kiểm tra và đảm bảo gói tin không bị mất mát, đến nơi theo đúng thứ tự, có cơ chế truyền lại nếu lỗi.
   - ⚠️ **Bẫy thi:** Đề thường đảo ngược chức năng của TCP và IP cho nhau. Hãy nhớ: <span style="color: red; text-decoration: underline;">IP là "Người giao hàng" (chỉ cần biết địa chỉ), TCP là "Quản lý chất lượng" (đảm bảo hàng nguyên vẹn)</span>.

2. **Địa chỉ IPv4 vs IPv6**:
   - **IPv4**: Dài 32-bit. Gồm 4 cụm số cách nhau bởi dấu chấm (VD: `192.168.1.1`).
   - **IPv6**: Dài 128-bit. Ra đời để giải quyết vấn đề cạn kiệt không gian địa chỉ IPv4. (VD: `2001:0db8:85a3::8a2e:0370:7334`).
   - ⚠️ **BẪY CỰC NGUY HIỂM:** Đề thi sẽ đưa ra 4 địa chỉ IPv4 và hỏi địa chỉ nào hợp lệ. Em phải nhớ mỗi cụm số IPv4 <span style="color: red; text-decoration: underline;">chỉ chạy từ 0 đến 255</span>. (VD: `192.168.1.256` hoặc `192.-1.1.1` là <span style="color: red; text-decoration: underline;">hoàn toàn sai do vượt quá 255 hoặc bị âm</span>).

3. **<span style="color: blue; text-decoration: underline;">DNS (Domain Name System)</span>**:
   - Hệ thống phân giải tên miền.
   - **Vai trò**: Dịch một tên miền dễ nhớ (vd: `google.com`) sang dãy IP khô khan (vd: `142.250.190.46`) để máy tính định tuyến được.
   - ⚠️ **Bẫy thi:** "<span style="color: red; text-decoration: underline;">DNS giúp tăng tốc độ mạng Internet</span>" -> **SAI**. DNS chỉ làm nhiệm vụ "Cuốn danh bạ điện thoại", nó giúp con người dễ sử dụng web hơn chứ không làm mạng nhanh hơn. Đôi khi server DNS lỗi, mạng vẫn bình thường nhưng em không vào web bằng chữ được (phải gõ số IP).
"""

content_2 = r"""# CHUYÊN ĐỀ 2: TRÍ TUỆ NHÂN TẠO (AI) VÀ HỌC MÁY
*(Cập nhật theo định hướng đề thi THPT QG 2025)*

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) cốt lõi phải nhớ.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: "Bẫy" đánh lừa trong các câu hỏi trắc nghiệm khách quan & Đúng/Sai.

---

## 1. KHÁI NIỆM TRÍ TUỆ NHÂN TẠO (AI)
<span style="color: blue; text-decoration: underline;">Trí tuệ nhân tạo (AI - Artificial Intelligence)</span> là nhánh khoa học máy tính với mục tiêu tạo ra máy móc có khả năng mô phỏng các hoạt động trí tuệ của con người (như học hỏi, lập luận, hiểu ngôn ngữ, tự sửa lỗi, sáng tạo nghệ thuật).

### Các loại AI:
- <span style="color: blue; text-decoration: underline;">AI hẹp (Weak AI / Narrow AI)</span>: Chỉ được huấn luyện để giải quyết **một công việc cụ thể** (VD: AI đánh cờ, ChatGPT viết văn bản, hệ thống nhận diện khuôn mặt). **Tất cả AI hiện nay đều là AI hẹp**.
- <span style="color: blue; text-decoration: underline;">AI rộng (Strong AI / General AI)</span>: Cỗ máy có trí thông minh bao quát, ngang ngửa con người, có thể làm mọi việc con người làm. (Hiện chỉ có trong lý thuyết và phim ảnh khoa học viễn tưởng).

⚠️ **BẪY TRẮC NGHIỆM ĐÚNG/SAI:**
- Mệnh đề: "<span style="color: red; text-decoration: underline;">AI hiện nay đã phát triển đến mức có cảm xúc, ý thức và suy nghĩ độc lập giống hệt con người</span>". -> **SAI**. AI hiện tại (ngay cả ChatGPT tiên tiến nhất) chỉ là các mô hình toán học và xác suất khổng lồ. Nó sinh ra văn bản dựa trên việc dự đoán từ tiếp theo, hoàn toàn <span style="color: red; text-decoration: underline;">không có nhận thức hay cảm xúc</span>.
- Mệnh đề: "<span style="color: red; text-decoration: underline;">Mọi chương trình máy tính tự động đều là AI</span>". -> **SAI**. Một chương trình tính lương nhân viên tự động (bằng if-else, công thức toán) không phải là AI. AI phải có yếu tố mô phỏng tư duy (học từ dữ liệu, thích nghi với tình huống chưa từng lập trình trước).

---

## 2. HỌC MÁY (MACHINE LEARNING) VÀ HỌC SÂU (DEEP LEARNING)
Học sinh rất dễ bị nhầm lẫn 3 khái niệm: AI, Học máy, Học sâu. Hãy nhớ cấu trúc bao hàm (tập hợp con): **AI > Học máy > Học sâu**.

1. **<span style="color: blue; text-decoration: underline;">Học máy (Machine Learning)</span>**:
   - Là phương pháp thay vì lập trình tĩnh (viết hàng triệu lệnh IF-ELSE cho máy), ta cung cấp cho máy tính <span style="color: blue; text-decoration: underline;">một lượng lớn Dữ liệu (Data)</span> để nó **tự rút ra quy luật** và mô hình toán học.
   - Ví dụ: Dạy máy phân biệt chó mèo bằng cách cho nó xem 10,000 ảnh chó và 10,000 ảnh mèo kèm nhãn dán.

2. **<span style="color: blue; text-decoration: underline;">Học sâu (Deep Learning)</span>**:
   - Là một mạng lưới thần kinh nhân tạo (Artificial Neural Network) nhiều lớp (nhiều tàng ẩn), mô phỏng cấu trúc neuron của não bộ con người.
   - Cần lượng dữ liệu khổng lồ (Big Data) và năng lực tính toán cực lớn (GPU mạnh mẽ). ChatGPT là một sản phẩm của Deep Learning.

⚠️ **BẪY THI:**
- "<span style="color: red; text-decoration: underline;">Học máy là một ngành khoa học độc lập, rộng lớn hơn Trí tuệ nhân tạo</span>". -> **SAI**. Học máy chỉ là một cách (phương pháp) để đạt được Trí tuệ nhân tạo. AI chứa Học máy.

---

## 3. CÁC LĨNH VỰC ỨNG DỤNG THỰC TẾ TRỌNG TÂM CỦA AI
Đề thi rất hay đưa ra một tình huống thực tế và yêu cầu học sinh phân loại công nghệ AI đang được áp dụng.

1. **<span style="color: blue; text-decoration: underline;">Thị giác máy tính (Computer Vision)</span>**:
   - Khả năng "nhìn" và hiểu ý nghĩa hình ảnh/video của máy tính.
   - **Ứng dụng**: Nhận diện khuôn mặt mở khóa FaceID, ô tô tự lái (nhận diện biển báo, vạch kẻ đường, người đi bộ), hệ thống chẩn đoán y tế qua ảnh X-Quang, quét lỗi linh kiện trên băng chuyền nhà máy.

2. **<span style="color: blue; text-decoration: underline;">Xử lý ngôn ngữ tự nhiên (Natural Language Processing - NLP)</span>**:
   - Khả năng "đọc/nghe" và "hiểu/nói" ngôn ngữ của loài người một cách tự nhiên.
   - **Ứng dụng**: Chatbot (ChatGPT, Gemini), Dịch máy tự động (Google Translate), Trợ lý ảo (Siri, Alexa, Google Assistant), Nhận diện giọng nói thành văn bản.

3. **<span style="color: blue; text-decoration: underline;">Hệ chuyên gia (Expert System)</span>**:
   - Phần mềm máy tính mô phỏng kỹ năng ra quyết định của một chuyên gia giỏi là con người trong một lĩnh vực rất hẹp. Hệ thống gồm: **Cơ sở tri thức (Chứa kiến thức chuyên gia)** và **Động cơ suy diễn (Chứa các luật logic)**.
   - **Ứng dụng**: Hệ thống MYCIN tư vấn y tế (bác sĩ nhập triệu chứng -> máy suy diễn ra bệnh và phác đồ điều trị), Hệ thống chẩn đoán lỗi phần cứng máy bay.

⚠️ **BẪY TÌNH HUỐNG (CỰC KỲ DỄ SAI):**
- Đề hỏi: "Hệ thống Google Translate tự động dịch đoạn văn bản tiếng Anh sang tiếng Việt đang áp dụng công nghệ AI cốt lõi nào?"
- A. Thị giác máy tính
- B. Xử lý ngôn ngữ tự nhiên (NLP)
- C. Hệ chuyên gia
- **Đáp án là B**. Học sinh rất dễ chọn C (Hệ chuyên gia) vì lập luận "máy làm chuyên gia dịch thuật". -> <span style="color: red; text-decoration: underline;">Bẫy rất sâu</span>. Hệ chuyên gia là dựa trên luật logic IF-THEN (Nếu sốt > 39 độ THÌ bị cảm), còn dịch thuật là xử lý thống kê ngôn ngữ NLP.
"""

content_3 = r"""# CHUYÊN ĐỀ 3: CƠ SỞ DỮ LIỆU (CSDL) VÀ SQL
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
"""

content_4 = r"""# CHUYÊN ĐỀ 4: HTML VÀ CSS CĂN BẢN
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
"""

content_5 = r"""# CHUYÊN ĐỀ 5: BẢO MẬT, AN TOÀN HỆ THỐNG VÀ KHẮC PHỤC SỰ CỐ
*(Cập nhật theo định hướng đề thi THPT QG 2025)*

*Chú giải:*
- <span style="color: blue; text-decoration: underline;">Gạch chân màu xanh</span>: Các từ khóa (Key word) cốt lõi phải nhớ.
- <span style="color: red; text-decoration: underline;">Gạch chân màu đỏ</span>: "Bẫy" đánh lừa trong các câu hỏi trắc nghiệm khách quan & Đúng/Sai.

---

## 1. PHÂN BIỆT BẢO MẬT (SECURITY) VÀ AN TOÀN (SAFETY) CSDL
Đây là cặp khái niệm dễ gây mất điểm nhất trong phần lý thuyết cuối của đề thi môn Tin Học. Học sinh phải phân định thật rõ hai yếu tố này.

1. **<span style="color: blue; text-decoration: underline;">Bảo mật (Security)</span>**:
   - Là chống lại các mối đe dọa **cố ý, mang tính phá hoại**.
   - Các tác nhân: Hacker tấn công, nhân viên công ty cố tình trộm dữ liệu, mã độc (Virus, Ransomware) mã hóa file đòi tiền chuộc.
   - **Giải pháp bảo mật**: Đặt mật khẩu mạnh, Phân quyền người dùng (Authorization), Tường lửa (Firewall), Mã hóa dữ liệu truyền đi (Mã hóa đầu cuối).

2. **<span style="color: blue; text-decoration: underline;">An toàn dữ liệu (Safety / Reliability)</span>**:
   - Là bảo vệ dữ liệu khỏi các sự cố **khách quan, sự cố ngoài ý muốn, lỗi do thiên nhiên hoặc vô ý**.
   - Các tác nhân: Ổ cứng đột nhiên hỏng, chập cháy nổ, cúp điện đột ngột đang lưu dở, lũ lụt, người dùng lỡ tay bấm Delete.
   - **Giải pháp an toàn**: <span style="color: blue; text-decoration: underline;">Sao lưu dữ liệu định kỳ (Backup)</span>, Lắp bộ lưu điện UPS, Xây dựng hệ thống dự phòng (Redundancy).

⚠️ **BẪY CHÍ TỬ TRONG ĐỀ:**
- Tình huống: "Ngân hàng A mua hệ thống tường lửa (Firewall) triệu đô và dùng thuật toán mã hóa 256-bit tiên tiến nhất để bảo vệ CSDL khách hàng. Do đó, ngân hàng không cần phải Sao lưu (Backup) dữ liệu mỗi ngày nữa vì hệ thống đã quá an toàn".
- -> Mệnh đề này **SAI HOÀN TOÀN**. Tường lửa và Mã hóa chỉ là giải pháp <span style="color: red; text-decoration: underline;">Bảo mật (chống Hacker)</span>. Nếu tòa nhà ngân hàng bị cháy, hay máy chủ hỏng ổ cứng (sự cố khách quan), không có bản Backup thì dữ liệu sẽ mất vĩnh viễn! Bảo mật không thể thay thế cho An toàn.

---

## 2. MẬT MÃ HỌC VÀ CHỮ KÝ SỐ
Các khái niệm mã hóa truyền thông tin trên mạng Internet.

1. **<span style="color: blue; text-decoration: underline;">Mã hóa đối xứng (Symmetric Encryption)</span>**:
   - Người gửi và người nhận dùng **CÙNG MỘT CHÌA KHÓA** (Key) duy nhất để vừa Khóa (Mã hóa) vừa Mở khóa (Giải mã).
   - <span style="color: blue; text-decoration: underline;">Ưu điểm</span>: Tốc độ mã hóa cực nhanh.
   - <span style="color: blue; text-decoration: underline;">Nhược điểm</span>: Bài toán "Làm sao trao chìa khóa cho nhau qua mạng mà không bị hacker đứng giữa bắt được?". Rất khó quản lý chìa khóa nếu có hàng vạn người dùng.

2. **<span style="color: blue; text-decoration: underline;">Mã hóa bất đối xứng (Asymmetric Encryption - Public Key)</span>**:
   - Mỗi người tạo ra **MỘT CẶP KHÓA** có liên hệ toán học mật thiết: <span style="color: blue; text-decoration: underline;">Khóa công khai (Public Key)</span> và <span style="color: blue; text-decoration: underline;">Khóa bí mật (Private Key)</span>.
   - Nguyên tắc thép: Khóa công khai phơi bày cho cả thế giới, Khóa bí mật chỉ mình mình giữ. **Cái gì khóa bằng Public thì CHỈ CÓ THỂ mở bằng Private tương ứng**.
   - <span style="color: blue; text-decoration: underline;">Ứng dụng thực tế</span>: Giao thức HTTPS trên trình duyệt web sử dụng loại mã hóa này.
   - ⚠️ **BẪY TRẮC NGHIỆM:** "A muốn gửi thư mật cho B. A sẽ dùng chìa khóa nào để mã hóa?" -> Đáp án là: **A phải dùng Khóa công khai (Public Key) của B** để khóa hộp. Khi hộp tới nơi, chỉ có B (người duy nhất giữ Khóa bí mật Private Key của B) mới mở được. (Đừng bao giờ chọn là "A dùng khóa bí mật của A để khóa").

3. **<span style="color: blue; text-decoration: underline;">Chữ ký số (Digital Signature)</span>**:
   - Ngược lại với quy trình mã hóa gửi thư mật. Chữ ký số dùng để **chứng minh danh tính** của người gửi văn bản và đảm bảo văn bản không bị sửa đổi trên đường truyền.
   - **Quy trình**: Người gửi sẽ dùng **Khóa bí mật (Private Key) CỦA CHÍNH MÌNH** để ký (khóa) một đoạn mã băm của văn bản. Mọi người nhận đều có thể dùng Khóa công khai của người gửi để mở ra kiểm chứng. Nếu mở được -> Đúng là anh ta gửi.
   - ⚠️ **BẪY THI:** Chữ ký số <span style="color: red; text-decoration: underline;">KHÔNG dùng để giữ bí mật nội dung văn bản</span>. Nó chỉ dùng để chứng minh nguồn gốc và tính toàn vẹn (văn bản chưa bị sửa đổi).
"""

with open(os.path.join(folder, '1_MangMayTinh.md'), 'w', encoding='utf-8') as f: f.write(content_1)
with open(os.path.join(folder, '2_TriTueNhanTao.md'), 'w', encoding='utf-8') as f: f.write(content_2)
with open(os.path.join(folder, '3_CoSoDuLieu.md'), 'w', encoding='utf-8') as f: f.write(content_3)
with open(os.path.join(folder, '4_HTML_CSS.md'), 'w', encoding='utf-8') as f: f.write(content_4)
with open(os.path.join(folder, '5_BaoMatAnToan.md'), 'w', encoding='utf-8') as f: f.write(content_5)

print("Đã tạo 5 file thành công")

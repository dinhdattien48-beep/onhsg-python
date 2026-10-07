# CHUYÊN ĐỀ 1: MẠNG MÁY TÍNH VÀ INTERNET
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

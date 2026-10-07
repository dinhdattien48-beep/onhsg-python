# CHUYÊN ĐỀ 5: BẢO MẬT, AN TOÀN HỆ THỐNG VÀ KHẮC PHỤC SỰ CỐ
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

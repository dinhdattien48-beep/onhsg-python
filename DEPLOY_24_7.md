# 🚀 Hướng Dẫn Triển Khai Web HSG Python Chạy 24/24 (Render & Hugging Face)

Tất cả cấu hình Docker, cơ chế chống ngủ (Keep-Alive), tự động nạp API Key của giáo viên và bảo lưu tiến độ học sinh vào trình duyệt đã được tích hợp sẵn 100%. Bạn chỉ cần thực hiện các thao tác click chuột sau trong 2 phút:

---

## 📌 BƯỚC 1: Đẩy Dự Án Lên GitHub (30 giây)

1. Mở trình duyệt truy cập: [https://github.com/new](https://github.com/new)
2. Nhập tên Repository: `onhsg-python` (để chế độ **Public** hoặc **Private** đều được).
3. **Bỏ qua tất cả các ô chọn** (không tích Add README, .gitignore...) -> Bấm nút xanh **Create repository**.
4. Mở cửa sổ Terminal tại thư mục `Onhsg` trên máy tính và copy 3 lệnh sau dán vào chạy (thay `USERNAME` bằng tên GitHub của bạn):
   ```bash
   git branch -M main
   git remote add origin https://github.com/USERNAME/onhsg-python.git
   git push -u origin main
   ```

---

## 🌐 CÁCH 1: Triển Khai Lên Render.com (Khuyên dùng - 24/24 Tự Động)

Render tương thích hoàn toàn với file `render.yaml` và `Dockerfile` đã được tạo sẵn trong dự án.

1. Truy cập [https://dashboard.render.com](https://dashboard.render.com) và đăng nhập bằng tài khoản GitHub.
2. Bấm nút **New +** ở góc phải trên cùng ➔ Chọn **Blueprint** (hoặc **Web Service**).
   - *Nếu chọn Blueprint*: Chọn repository `onhsg-python` ➔ Render sẽ tự động đọc file `render.yaml` và cấu hình tất cả cho bạn.
   - *Nếu chọn Web Service*: Chọn repo `onhsg-python`, chọn môi trường **Docker**, Region: **Singapore**.
3. Tại phần **Environment Variables** (Biến môi trường), thêm biến:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Dán API Key Gemini của bạn vào đây.
   - *(Tùy chọn)*: `GEMINI_MODEL` = `gemini-3.8-flash` (đã có mặc định).
4. Bấm **Create Web Service** (hoặc **Apply Blueprint**).
5. **Hoàn thành!** Render sẽ build Docker và cấp cho bạn một đường link dạng:
   `https://onhsg-python.onrender.com`

> ⚡ **Cơ chế giữ thức 24/24:** Backend đã tích hợp sẵn tiến trình ngầm (Background Task). Cứ mỗi 10 phút, server sẽ tự động ping vào URL chính mình qua endpoint `/health` để giữ cho dịch vụ luôn hoạt động liên tục 24/24 ngay cả khi bạn tắt máy tính.

---

## 🤗 CÁCH 2: Triển Khai Lên Hugging Face Spaces (Chạy 24/24 Ổn Định)

Hugging Face Spaces cung cấp hosting container Docker miễn phí, không bao giờ bị sleep.

1. Truy cập [https://huggingface.co/spaces](https://huggingface.co/spaces) (đăng nhập hoặc tạo tài khoản miễn phí).
2. Bấm nút **Create new Space**.
3. Điền thông tin:
   - **Space name**: `onhsg-python`
   - **Space SDK**: Chọn **Docker** (Blank)
   - **Space hardware**: Chọn **CPU basic • 2 vCPU • 16GB • Free**
   - **Visibility**: Chọn **Public**
   - Bấm **Create Space**.
4. Cài đặt API Key bảo mật:
   - Trong Space vừa tạo, bấm tab **Settings** ➔ Cuộn xuống mục **Variables and secrets**.
   - Bấm **New secret**:
     - Name: `GEMINI_API_KEY`
     - Value: Dán API Key Gemini của bạn vào.
5. Đẩy code từ máy lên Hugging Face Space:
   - Copy đường dẫn Git của Space (trong tab Space có sẵn), sau đó trong terminal máy tính chạy:
     ```bash
     git remote add hf https://huggingface.co/spaces/USERNAME/onhsg-python
     git push -f hf main
     ```
   - Hugging Face sẽ tự động build Dockerfile và mở web ở cổng `7860`.

---

## 🎯 CÁC TÍNH NĂNG ĐÃ ĐƯỢC TỐI ƯU SẴN CHO HỌC SINH

- **Học sinh dùng chung AI miễn phí:** Học sinh truy cập vào web chỉ việc viết code và bấm **🚀 Nộp bài**, AI Mentor sẽ tự động nhận xét và hướng dẫn tối ưu code ngay mà học sinh không cần nhập bất kỳ API key nào.
- **Bảo mật tuyệt đối:** API Key của bạn nằm an toàn trên biến môi trường máy chủ Cloud, giao diện web và API đều không để lộ Key.
- **Chống mất bài làm:** Toàn bộ lịch sử các bài làm đúng (AC 10/10) và từng đoạn code học sinh đang viết dở đều được tự động lưu vào `localStorage` của trình duyệt. Dù Cloud có khởi động lại, học sinh tải lại trang web vẫn thấy đầy đủ tiến độ và code của mình!

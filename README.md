# 🐍 HSG Python — Luyện thi Học Sinh Giỏi Tin học

Nền tảng dạy và luyện thi **Học Sinh Giỏi (HSG) Tin học** bằng ngôn ngữ **Python**, dành cho học sinh bắt đầu từ con số 0.

## ✨ Tính năng

- 📚 **8 chặng lộ trình** từ cơ bản đến nâng cao (24 bài tập)
- 🔫 **Góc Vũ Khí Python** — Dạy hàm Built-in tối ưu tốc độ code
- ⚡ **Chấm bài tự động 10 test cases** (AC/WA/TLE/RE)
- 🤖 **AI Mentor** (Google Gemini) nhận xét và gợi ý tối ưu code
- 💻 **Code Editor** với tô màu cú pháp Python (CodeMirror)
- 📊 **Theo dõi tiến độ** — đánh dấu bài đã hoàn thành
- 🎨 **Giao diện Dark Mode** hiện đại, responsive

## 🚀 Cài đặt và Khởi chạy

### Yêu cầu
- **Python 3.9+**
- **pip** (trình quản lý gói Python)

### Bước 1: Clone hoặc tải project

```bash
cd c:\Users\TDat\Desktop\KHKT\Onhsg
```

### Bước 2: Cài đặt thư viện Python

```bash
cd backend
pip install -r requirements.txt
```

### Bước 3: Khởi chạy server

```bash
cd backend
python main.py
```

Server sẽ chạy tại: **http://localhost:8000**

### Bước 4: Mở trình duyệt

Truy cập **http://localhost:8000** để bắt đầu học!

## ⚙️ Cấu hình AI Mentor & Bảo mật API Key

Bạn có thể cấu hình API Key của Google Gemini theo 2 cách:

1. **Trên Cloud / Máy chủ (Khuyên dùng - Bảo mật tuyệt đối cho học sinh):**
   - Đặt biến môi trường trên server (Render, Hugging Face Spaces, v.v.):
     - `GEMINI_API_KEY`: API Key của bạn (lấy miễn phí tại [Google AI Studio](https://aistudio.google.com/apikey))
     - `GEMINI_MODEL`: Model sử dụng (mặc định: `gemini-3.8-flash`)
   - Khi đó, học sinh truy cập web sẽ tự động sử dụng AI Mentor trên server mà không cần nhập key và không lo bị lộ key.

2. **Chạy cục bộ (Local):**
   - Tạo file `.env` từ `.env.example` và điền `GEMINI_API_KEY=...`

## ☁️ Hướng dẫn Triển khai Cloud (Chạy 24/24 Miễn phí)

Dự án đã được đóng gói sẵn để deploy lên các nền tảng Cloud chỉ với vài cú click:

### Cách 1: Triển khai lên Render.com (Khuyên dùng)
1. Đẩy mã nguồn lên kho lưu trữ **GitHub**.
2. Đăng nhập [Render.com](https://render.com/) -> Chọn **New +** -> **Blueprint**.
3. Chọn repository của bạn. Render sẽ tự động đọc file [render.yaml](file:///c:/Users/TDat/Desktop/KHKT/Onhsg/render.yaml).
4. Trong phần thiết lập biến môi trường, nhập giá trị cho `GEMINI_API_KEY`.
5. Nhấn **Apply**. Ứng dụng sẽ tự động build qua [Dockerfile](file:///c:/Users/TDat/Desktop/KHKT/Onhsg/Dockerfile) và cung cấp đường link HTTPS truy cập 24/24!

### Cách 2: Triển khai lên Hugging Face Spaces (Docker)
1. Tạo một Space mới trên [Hugging Face Spaces](https://huggingface.co/spaces) với SDK là **Docker** (Blank).
2. Đẩy code lên Space repo (hoặc liên kết với GitHub).
3. Vào mục **Settings** của Space -> **Variables and secrets** -> Thêm Secret:
   - Name: `GEMINI_API_KEY`
   - Value: `<API_KEY_CỦA_BẠN>`
4. Không gian sẽ tự động build từ [Dockerfile](file:///c:/Users/TDat/Desktop/KHKT/Onhsg/Dockerfile) chạy trên cổng `7860`.

> **Bảo lưu tiến độ học sinh:** Hệ thống đã tích hợp cơ chế tự động đồng bộ danh sách bài hoàn thành (AC 10/10) vào `localStorage` của trình duyệt. Dù server cloud miễn phí có khởi động lại hoặc xoá dữ liệu tạm thì học sinh vẫn giữ nguyên toàn bộ tiến độ học tập!

## 📂 Cấu trúc dự án

```
Onhsg/
├── backend/
│   ├── main.py              # FastAPI server chính
│   ├── judge.py             # Hệ thống chấm bài tự động
│   ├── ai_mentor.py         # Tích hợp AI Gemini
│   ├── database.py          # SQLite quản lý tiến độ
│   ├── seed_data.py         # Dữ liệu giáo trình 8 chặng
│   └── requirements.txt     # Thư viện Python
├── frontend/
│   ├── index.html           # Giao diện chính (SPA)
│   ├── styles.css           # CSS Dark theme
│   └── app.js               # Logic frontend
└── README.md                # Hướng dẫn sử dụng
```

## 📖 Lộ trình 8 chặng

| Chặng | Chủ đề | Vũ Khí Python |
|-------|--------|---------------|
| 🚀 1 | Làm quen Python & Nhập xuất | `map()`, `sys.stdin.readline` |
| 🔀 2 | Rẽ nhánh & Toán học | `min()`, `max()`, `pow(a,b,mod)` |
| 🔄 3 | Vòng lặp & Khử vòng lặp | `sum()`, công thức $O(1)$ |
| 📝 4 | Xử lý Xâu (String) | `s[::-1]`, `.split()`, `.join()` |
| 📊 5 | List & Set/Dict | `set`, `Counter` |
| 🔢 6 | Số học HSG | `math.isqrt()`, `math.gcd()` |
| 📈 7 | Sắp xếp & Nhị phân | `sorted(key=lambda)`, `bisect` |
| ⚡ 8 | Prefix Sum, Two Pointers, Đệ quy | `accumulate`, `@lru_cache` |

## 🧪 Hệ thống chấm bài

Mỗi bài tập có **10 test cases** tự động:
- **Test 1-3:** Test mẫu, dữ liệu nhỏ
- **Test 4-7:** Test biên (edge cases)
- **Test 8-10:** Test hiệu năng (stress test)

Trạng thái chấm:
- 🟢 **AC** (Accepted) — Đúng
- 🔴 **WA** (Wrong Answer) — Sai kết quả
- 🟡 **TLE** (Time Limit Exceeded) — Quá thời gian
- 🟣 **RE** (Runtime Error) — Lỗi chạy

## 🛠️ Công nghệ sử dụng

- **Backend:** Python, FastAPI, SQLite
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Code Editor:** CodeMirror 5
- **AI:** Google Gemini (google-genai SDK)
- **Math Rendering:** KaTeX
- **Markdown:** Marked.js

## 📝 License

Dự án phục vụ mục đích giáo dục — Luyện thi HSG Tin học.

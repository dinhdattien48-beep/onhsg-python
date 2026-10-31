# BẢN ĐỒ DỰ ÁN (PROJECT MAP)

Tài liệu định tuyến cấu trúc duy nhất của dự án. Mọi tác vụ đọc và chỉnh sửa frontend/backend đều tra cứu từ bản đồ này trước khi thao tác file.

---

## 1. CÂY THƯ MỤC (FOLDER TREE)

```text
Onhsg/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── backend/
│   ├── main.py
│   ├── ai_mentor.py
│   ├── auth.py
│   ├── azota_parser.py
│   ├── classroom.py
│   ├── database.py
│   ├── debugger.py
│   ├── judge.py
│   ├── seed_data.py
│   ├── thpt_quiz_data.py
│   ├── test_smtp.py
│   └── requirements.txt
├── Ôn TN THPT QGia/
│   └── ChuyenDe/
│       ├── 1_MangMayTinh.md
│       ├── 2_TriTueNhanTao.md
│       ├── 3_CoSoDuLieu.md
│       ├── 3_CoSoDuLieu_Exercises.md
│       ├── 4_HTML_CSS.md
│       └── 5_BaoMatAnToan.md
├── [NHÓM TÀI NGUYÊN TĨNH & CẤU HÌNH BỎ QUA]
│   ├── image.png, LiThuyet TN THPT.docx
│   ├── .env, .env.example, Dockerfile, render.yaml
│   ├── README.md, DEPLOY_24_7.md, state.md, temp_content.txt
│   ├── scratch_update*.py, hsg_python.db
│   └── Thư viện CDN ngoài (CodeMirror, Marked, KaTeX) nạp qua thẻ link/script
└── project-map.md
```

---

## 2. DANH MỤC FILE GIAO DIỆN & KỊCH BẢN (HTML / CSS / JS)

Mỗi file đúng 1 dòng mô tả chức năng cốt lõi:

- `frontend/index.html`: Khung HTML duy nhất chứa toàn bộ thanh điều hướng, cây nội dung, khu vực làm việc và các cửa sổ chức năng.
- `frontend/styles.css`: Hệ thống thiết kế toàn cục (màu sắc, viền, khoảng cách, font chữ, hiệu ứng) quy định diện mạo giao diện.
- `frontend/app.js`: Toàn bộ logic tương tác người dùng, nạp dữ liệu từ backend, chấm trắc nghiệm, chạy code và gọi trợ lý.

---

## 3. NGUYÊN TẮC VẬN HÀNH (WORKFLOW PROTOCOL)

1. **Tra cứu trước**: Khi nhận yêu cầu mới, chỉ đọc `project-map.md` để xác định chính xác file cần can thiệp.
2. **Sửa đích danh**: Chỉ mở và sửa đúng phân đoạn code của file đích, tuyệt đối không quét lại toàn bộ thư mục.
3. **Chuẩn phong cách**: Tách biệt UI vào `styles.css`, không viết CSS inline trong JS hay HTML; tuân thủ triệt để chủ nghĩa Tối giản (Brutalism / Clean UI).

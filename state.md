# Session State — HSG Python

## Đã hoàn thành:
- Toàn bộ codebase v1: Backend (FastAPI + SQLite + Judge + AI Mentor) + Frontend (SPA dark mode)
- 8 chặng lộ trình, 24 bài tập, hệ thống chấm 10 test cases
- Góc Vũ Khí Python, tích hợp AI Gemini, CodeMirror editor
- Cấu hình deploy: Dockerfile, render.yaml
- README.md hoàn chỉnh
- **Nested Accordion Sidebar:** 4 folder Level-1 (Ôn HSG / Ôn TN THPT / Luyện Đề / BTap GV giao)
  - CSS mới: `.folder-group`, `.folder-header`, `.folder-content`, `.folder-arrow`, `.folder-placeholder` (styles.css ~line 595)
  - JS: `renderSidebar()` refactor dùng helper `makeFolder()` (app.js ~line 316)
  - Folder "Ôn Học Sinh Giỏi" mở mặc định, 3 folder còn lại đóng, có placeholder text

## Đang làm dở:
- (Không có)

## Bước tiếp theo:
- Chờ yêu cầu: thêm bài tập vào 3 folder placeholder, hoặc task khác
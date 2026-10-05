---
name: session-state
description: Duy trì trạng thái công việc thông qua file state.md để tránh phải nhắc lại bối cảnh dự án ở các phiên chat mới.
---
# Session State Rules
1. Ở mỗi cuối câu trả lời quan trọng, cập nhật trạng thái ngắn gọn vào file `state.md` của dự án với cấu trúc:
   - **Đã hoàn thành:** ...
   - **Đang làm dở:** ...
   - **Bước tiếp theo:** ...
2. Khi bắt đầu phiên chat mới, chỉ đọc file `state.md` này để khôi phục ngữ cảnh thay vì đọc lại toàn bộ lịch sử trò chuyện cũ.
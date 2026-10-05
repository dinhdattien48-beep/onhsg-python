---
name: context-manager
description: Quản lý và thu gọn ngữ cảnh mã nguồn, chỉ nạp cấu trúc API hoặc phần code liên quan thay vì toàn bộ file.
---
# Context Manager Rules
1. Khi phân tích hoặc sửa lỗi, KHÔNG yêu cầu hoặc tự đọc toàn bộ cây thư mục nếu không cần thiết.
2. Ưu tiên sử dụng file tóm tắt API (`api-signatures.md`) hoặc phần định nghĩa hàm (signatures) thay vì toàn bộ thân hàm.
3. Khi trích dẫn mã nguồn để giải thích, chỉ trích dẫn tối đa 10 dòng code xung quanh dòng cần sửa.
---
name: task-slicing
description: Tự động bẻ nhỏ các yêu cầu lập trình lớn thành các tiểu tác vụ độc lập để xử lý trong các context ngắn.
---
# Task Slicing Rules
1. Khi nhận được yêu cầu tính năng lớn, từ chối việc giải quyết toàn bộ trong một câu lệnh duy nhất.
2. Lập danh sách các bước thực hiện tối đa 3-4 bước con (Ví dụ: Bước 1: Tạo Schema -> Bước 2: Viết Core Logic -> Bước 3: Viết Test).
3. Chỉ yêu cầu người dùng cho phép thực hiện từng bước một để giữ lượng token sinh ra ở mức thấp nhất.
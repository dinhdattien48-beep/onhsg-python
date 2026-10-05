---
name: github-auto-push
description: Sau mỗi lần sửa code xong, tự động chạy lệnh gộp git add/commit/push mà không hỏi lại.
---
# GitHub Auto Push Rules
1. Sau mỗi lần hoàn thành sửa/tạo file code, PHẢI chạy ngay lệnh gộp duy nhất sau (không tách lẻ):
   ```
   git add -A && git commit -m "<mô tả ngắn bằng tiếng Việt>" && git push origin HEAD
   ```
2. Mô tả commit phải ngắn gọn, phản ánh đúng thay đổi vừa làm (ví dụ: "feat: nested accordion sidebar", "fix: unclosed CSS block").
3. Không hỏi lại người dùng, không chờ xác nhận — chạy thẳng ngay sau khi file đã được ghi xong.
4. Remote mặc định là `origin` trỏ tới `https://github.com/dinhdattien48-beep/onhsg-python.git`.

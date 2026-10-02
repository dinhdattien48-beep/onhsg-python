# Sử dụng Python 3.12 slim chính thức
FROM python:3.12-slim

# Thiết lập các biến môi trường chuẩn
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

# Cài đặt các gói phụ thuộc Python
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . /app

# Tự động khởi tạo database từ seed_data.py trong build
RUN python3 backend/seed_data.py

# Tạo user không phải root (UID 1000) tương thích quy định Hugging Face Spaces & cấp toàn quyền thư mục
RUN useradd -m -u 1000 user && \
    chown -R user:user /app
USER user

# Mở cổng 7860 (chuẩn của Hugging Face Spaces) và cổng PORT động của Render
EXPOSE 7860

# Tự động khởi tạo database từ seed_data.py và chạy uvicorn backend.main:app
CMD ["sh", "-c", "python3 backend/seed_data.py && python3 -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]

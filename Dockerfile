# 1. Base image
FROM python:3.11-slim

# 2. Ortam değişkenleri (hata mesajlarını ve buffer’ı optimize eder)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Çalışma dizini
WORKDIR /app

# 4. Sistem bağımlılıkları (opsiyonel, bazı kütüphaneler için gerekli)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# 5. Python bağımlılıklarını yükle
COPY app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir tiktoken protobuf


# 6. Uygulama dosyalarını kopyala
COPY app/ .

# 7. Uvicorn ile production modda çalıştır
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2015", "--workers", "4", "--proxy-headers"]
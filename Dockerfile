# Python 3.11 tabanlı resmi hafif (slim) imaj
FROM python:3.11-slim

# Konteyner içindeki çalışma dizini
WORKDIR /app

# PyMuPDF ve Tesseract OCR için gerekli Linux kütüphanelerini kur
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını (data ve src dahil) kopyala
COPY . .

# Streamlit varsayılan portunu aç
EXPOSE 8501

# Container başlatıldığında Streamlit uygulamasını ayağa kaldır
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

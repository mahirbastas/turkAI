# Kullanılacak temel imajı belirtin
FROM python:3.9

# Uygulama kodunu Docker container'ına kopyalayın
COPY . /app
WORKDIR /app

# Gerekli Python kütüphanelerini yükleyin
RUN pip install Flask pika

# Flask uygulamasını başlatın
CMD ["python", "app.py"]

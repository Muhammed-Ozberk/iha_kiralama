# Temel imaj olarak Python kullanıyoruz
FROM python:3.12-slim

# Çalışma dizinini belirleyelim
WORKDIR /app

# Gereksinimlerinizi yüklemeden önce proje dosyalarını kopyalayalım
COPY requirements.txt .

# Gereksinimleri yükleyelim
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını konteynıra kopyalayalım
COPY . .

# Django'nun 8000 portunu açalım
EXPOSE 8000

# Wait-for-it aracını projenize dahil ediyorsanız, konteynıra kopyalayalım
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Uygulamayı başlatırken migration'ları çalıştıracağız
CMD /app/wait-for-it.sh postgres:5432 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000

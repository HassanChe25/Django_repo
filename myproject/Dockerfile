FROM python:3.12-slim

WORKDIR /app

# تثبيت المكتبات الأساسية
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات
COPY myproject/requirements.txt /app/

# تثبيت dependencies
RUN pip install --no-cache-dir -r requirements.txt

# نسخ المشروع كله
COPY myproject/ /app/

# تشغيل الخادم (مثال)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

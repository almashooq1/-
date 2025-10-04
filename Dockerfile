# استخدام Python 3.9 كقاعدة
FROM python:3.9-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# تعيين مجلد العمل
WORKDIR /app

# تثبيت المتطلبات النظامية
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# نسخ ملفات التطبيق
COPY . .

# إنشاء المجلدات الضرورية
RUN mkdir -p static/uploads/students static/uploads/teachers static/images

# إنشاء مستخدم غير جذري
RUN useradd -m -u 1000 alawael && chown -R alawael:alawael /app
USER alawael

# المنفذ الذي سيعمل عليه التطبيق
EXPOSE 5000

# الأمر الافتراضي لتشغيل التطبيق
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "ملف موقع الاوائل 2:app"]

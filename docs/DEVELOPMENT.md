# نظام ERP - دليل التطوير

## بنية المشروع

```
alawael-erp/
├── app/                     # التطبيق الرئيسي
│   ├── models/              # نماذج قاعدة البيانات
│   ├── services/            # خدمات الأعمال
│   ├── routes/              # نقاط النهاية API
│   ├── utils/               # أدوات مساعدة
│   ├── templates/           # قوالب HTML
│   └── static/              # ملفات ثابتة
├── tests/                   # الاختبارات
├── docs/                    # التوثيق
├── config.py               # التكوينات
├── requirements.txt        # المكتبات
├── docker-compose.yml      # Docker
└── README.md               # الوثائق
```

## إعداد بيئة التطوير

### المتطلبات
- Python 3.10+
- PostgreSQL 14+
- MongoDB 6.0+
- Redis 7+
- Docker

### التثبيت
```bash
# 1. استنساخ المشروع
git clone https://github.com/almashooq1/-

# 2. البيئة الافتراضية
python -m venv venv
source venv/bin/activate

# 3. تثبيت المكتبات
pip install -r requirements.txt

# 4. إعداد البيئة
cp .env.example .env

# 5. قاعدة البيانات
flask db upgrade

# 6. التشغيل
python "ملف موقع الاوائل 2.py"
```

## Docker
```bash
docker-compose up -d
```

## الاختبارات
```bash
pytest
pytest --cov=app
```

## API Documentation
جميع endpoints تتطلب JWT token

### المصادقة
- POST /api/login
- POST /api/register

### الطلاب  
- GET /api/students
- POST /api/students
- GET /api/students/<id>

## النشر
```bash
docker-compose -f docker-compose.prod.yml up -d
```

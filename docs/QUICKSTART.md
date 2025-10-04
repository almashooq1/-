# دليل البدء السريع - Quick Start Guide

## مرحباً بك في نظام ERP مراكز الأوائل! 🎉

هذا الدليل سيساعدك على تشغيل النظام في أقل من 10 دقائق.

---

## المتطلبات الأساسية

قبل البدء، تأكد من تثبيت:
- ✅ Python 3.10 أو أحدث
- ✅ Docker و Docker Compose
- ✅ Git

---

## الطريقة الأولى: التشغيل باستخدام Docker (موصى به) 🐳

### الخطوة 1: استنساخ المشروع
```bash
git clone https://github.com/almashooq1/-
cd -
```

### الخطوة 2: إعداد ملف البيئة
```bash
cp .env.example .env
```

### الخطوة 3: تشغيل النظام
```bash
docker-compose up -d
```

### الخطوة 4: الوصول للنظام
انتظر دقيقة واحدة حتى يتم تشغيل جميع الخدمات، ثم:

- **التطبيق الرئيسي**: http://localhost:5000
- **Grafana Dashboard**: http://localhost:3000
  - Username: `admin`
  - Password: `alawael_grafana_2024`
- **Prometheus**: http://localhost:9090
- **RabbitMQ Management**: http://localhost:15672
  - Username: `alawael_user`
  - Password: `alawael_rabbit_2024`

### الخطوة 5: تهيئة البيانات الأولية
```bash
# تهيئة قاعدة البيانات
docker-compose exec app flask db upgrade

# تهيئة المهارات الـ 383
docker-compose exec app python init_skills.py

# إنشاء مستخدم مدير
docker-compose exec app python create_admin.py
```

**تم! 🎉** النظام جاهز الآن للاستخدام.

---

## الطريقة الثانية: التشغيل المحلي 💻

### الخطوة 1: استنساخ المشروع
```bash
git clone https://github.com/almashooq1/-
cd -
```

### الخطوة 2: إنشاء بيئة افتراضية
```bash
# على Windows
python -m venv venv
venv\Scripts\activate

# على Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### الخطوة 3: تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### الخطوة 4: إعداد قاعدة البيانات

#### تثبيت PostgreSQL (إذا لم يكن مثبتاً)
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
```

#### إنشاء قاعدة البيانات
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE alawael_erp;
CREATE USER alawael_user WITH PASSWORD 'alawael_pass_2024';
GRANT ALL PRIVILEGES ON DATABASE alawael_erp TO alawael_user;
\q
```

### الخطوة 5: إعداد ملف البيئة
```bash
cp .env.example .env
```

عدل ملف `.env`:
```ini
DATABASE_URI=postgresql://alawael_user:alawael_pass_2024@localhost:5432/alawael_erp
```

### الخطوة 6: تهيئة قاعدة البيانات
```bash
# تهيئة migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# تهيئة المهارات
python init_skills.py
```

### الخطوة 7: تشغيل التطبيق
```bash
python "ملف موقع الاوائل 2.py"
```

**افتح المتصفح:** http://localhost:5000

---

## تسجيل الدخول الأول 🔐

### الحساب الافتراضي للمدير:
- **البريد الإلكتروني**: `admin@alawael.com`
- **كلمة المرور**: `Admin@2024`

**⚠️ مهم:** غيّر كلمة المرور بعد أول تسجيل دخول!

---

## الخطوات التالية 🚀

بعد تسجيل الدخول:

### 1. إضافة السنة الدراسية
```
القائمة > الإعدادات > السنوات الدراسية > إضافة جديد
```

### 2. إنشاء الفصول
```
القائمة > الفصول > إضافة فصل جديد
```

### 3. إضافة موظف
```
القائمة > الموظفون > إضافة موظف
```

### 4. تسجيل أول طالب
```
القائمة > الطلاب > إضافة طالب
```

### 5. إجراء أول تقييم
```
افتح ملف الطالب > التقييمات > تقييم جديد
```

---

## اختبار المزايا 🧪

### اختبار الذكاء الاصطناعي
```bash
# افتح صفحة الذكاء الاصطناعي
http://localhost:5000/ai
```

### اختبار التقارير
```bash
# افتح صفحة التقارير
http://localhost:5000/reports
```

### اختبار تطبيق ولي الأمر
```bash
# افتح بوابة أولياء الأمور
http://localhost:5000/parent-portal
```

---

## الأوامر المفيدة 🛠️

### Docker Commands
```bash
# عرض حالة الخدمات
docker-compose ps

# عرض السجلات
docker-compose logs -f app

# إيقاف الخدمات
docker-compose down

# إعادة بناء الصور
docker-compose build

# حذف كل شيء وإعادة البدء
docker-compose down -v
docker-compose up -d --build
```

### Database Commands
```bash
# إنشاء migration جديد
flask db migrate -m "وصف التغيير"

# تطبيق migrations
flask db upgrade

# الرجوع لإصدار سابق
flask db downgrade
```

### تشغيل Celery
```bash
# Worker
celery -A celery_app worker --loglevel=info

# Beat (للمهام المجدولة)
celery -A celery_app beat --loglevel=info
```

---

## حل المشاكل الشائعة 🔧

### مشكلة: خطأ في الاتصال بقاعدة البيانات
**الحل:**
```bash
# تحقق من حالة PostgreSQL
docker-compose ps postgres
# أو
sudo systemctl status postgresql
```

### مشكلة: Port 5000 مستخدم
**الحل:**
```bash
# تغيير المنفذ في docker-compose.yml
ports:
  - "5001:5000"  # استخدم 5001 بدلاً من 5000
```

### مشكلة: خطأ في استيراد المكتبات
**الحل:**
```bash
# تحديث pip
pip install --upgrade pip

# إعادة تثبيت المكتبات
pip install -r requirements.txt --force-reinstall
```

### مشكلة: البيانات لا تظهر
**الحل:**
```bash
# تأكد من تشغيل migrations
flask db upgrade

# تهيئة البيانات الأساسية
python init_skills.py
```

---

## البيانات التجريبية (للتجربة) 🎭

### إنشاء بيانات تجريبية
```bash
# تشغيل السكريبت
python seed_data.py

# سيتم إنشاء:
# - 50 طالب
# - 20 موظف
# - 10 فصول
# - 100 تقييم
```

---

## الموارد المفيدة 📚

### التوثيق
- [دليل المستخدم الشامل](./USER_MANUAL.md)
- [توثيق API](./API.md)
- [معمارية النظام](./ARCHITECTURE.md)
- [دليل التطوير](./DEVELOPMENT.md)

### الدعم
- **البريد الإلكتروني**: support@alawael.com
- **الهاتف**: +966-XX-XXX-XXXX
- **GitHub Issues**: https://github.com/almashooq1/-/issues

---

## نصائح للأداء الأمثل ⚡

1. **استخدم Redis للتخزين المؤقت**
   ```bash
   # تأكد من تشغيل Redis
   docker-compose ps redis
   ```

2. **راقب استخدام الموارد**
   ```bash
   # افتح Grafana
   http://localhost:3000
   ```

3. **فعّل النسخ الاحتياطي التلقائي**
   ```bash
   # في ملف .env
   BACKUP_ENABLED=True
   ```

4. **استخدم HTTPS في الإنتاج**
   ```bash
   # أضف شهادة SSL في nginx/ssl/
   ```

---

## قائمة المراجعة للإعداد ✅

- [ ] تشغيل جميع الخدمات
- [ ] تهيئة قاعدة البيانات
- [ ] تحميل المهارات الـ 383
- [ ] إنشاء حساب مدير
- [ ] إضافة سنة دراسية
- [ ] إنشاء الفصول
- [ ] إضافة موظف
- [ ] تسجيل طالب
- [ ] إجراء تقييم
- [ ] تشغيل النسخ الاحتياطي
- [ ] تفعيل المراقبة (Prometheus/Grafana)

---

## البدء السريع في سطر واحد! ⚡

```bash
git clone https://github.com/almashooq1/- && cd - && docker-compose up -d
```

انتظر دقيقة، ثم افتح: http://localhost:5000

---

## أسئلة شائعة ❓

### س: كم يستغرق التثبيت؟
**ج:** 5-10 دقائق مع Docker، 15-20 دقيقة بدون Docker.

### س: هل أحتاج إلى خبرة برمجية؟
**ج:** لا، الدليل مصمم للمبتدئين. فقط اتبع الخطوات.

### س: هل يمكنني تجربة النظام بدون تثبيت؟
**ج:** نعم! سنوفر نسخة تجريبية عبر الإنترنت قريباً.

### س: كيف أحصل على المساعدة؟
**ج:** راسلنا على support@alawael.com أو افتح issue على GitHub.

---

## مبروك! 🎊

أنت الآن جاهز لاستخدام نظام ERP مراكز الأوائل للرعاية النهارية!

**التالي:** اقرأ [دليل المستخدم الشامل](./USER_MANUAL.md) لمعرفة المزيد من المزايا.

---

© 2024 مراكز الأوائل للرعاية النهارية - جميع الحقوق محفوظة

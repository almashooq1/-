# دليل أمان النظام

## نظرة عامة
هذا الدليل يوضح أفضل ممارسات الأمان لنظام مراكز الأوائل للرعاية النهارية.

## 1. أمان كلمات المرور

### للمستخدمين
- استخدم كلمات مرور قوية (8 أحرف على الأقل)
- استخدم مزيجًا من الأحرف الكبيرة والصغيرة والأرقام والرموز
- لا تشارك كلمة المرور مع أي شخص
- غيّر كلمة المرور بانتظام (كل 3 أشهر)
- لا تستخدم نفس كلمة المرور في أنظمة متعددة

### للمطورين
- جميع كلمات المرور مشفرة باستخدام bcrypt
- لا تخزن كلمات المرور كنص عادي
- استخدم salt قوي عشوائي لكل كلمة مرور

## 2. JWT Tokens

### الإعدادات الموصى بها
```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # انتهاء الصلاحية بعد ساعة
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # انتهاء refresh token بعد 30 يوم
```

### أفضل الممارسات
- احفظ tokens في localStorage أو sessionStorage
- لا ترسل tokens في URL
- تحقق من صلاحية token في كل طلب
- قم بإبطال tokens عند تسجيل الخروج

## 3. قاعدة البيانات

### الاتصال الآمن
- استخدم SSL/TLS للاتصال بقاعدة البيانات في الإنتاج
- لا تستخدم حساب root
- أنشئ مستخدم خاص بالتطبيق مع أقل الصلاحيات اللازمة

### النسخ الاحتياطي
- انسخ قاعدة البيانات يوميًا
- احفظ النسخ الاحتياطية في موقع آمن ومشفر
- اختبر استعادة النسخة الاحتياطية بانتظام

### مثال على النسخ الاحتياطي الآلي:
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/alawael"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="alawael_daycare"

# إنشاء نسخة احتياطية
pg_dump -U alawael_user $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# حذف النسخ الأقدم من 30 يوم
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

# تشفير النسخة الاحتياطية (اختياري)
gpg --encrypt --recipient admin@example.com $BACKUP_DIR/backup_$DATE.sql.gz
```

## 4. رفع الملفات

### التحقق من الملفات
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### أفضل الممارسات
- تحقق من نوع الملف (MIME type)
- حدّد حجم الملف المسموح
- استخدم أسماء ملفات آمنة (secure_filename)
- احفظ الملفات خارج مجلد التطبيق الرئيسي
- قم بفحص الملفات من الفيروسات

## 5. الحماية من الهجمات الشائعة

### SQL Injection
- استخدم SQLAlchemy ORM دائمًا
- لا تبنِ استعلامات SQL يدويًا من مدخلات المستخدم
- استخدم parameterized queries

```python
# ✅ آمن
user = User.query.filter_by(email=email).first()

# ❌ غير آمن
query = f"SELECT * FROM users WHERE email = '{email}'"
```

### XSS (Cross-Site Scripting)
- استخدم Jinja2 templates التي تفلتر المدخلات تلقائيًا
- لا تستخدم `|safe` إلا عند الضرورة
- تحقق من جميع مدخلات المستخدم

### CSRF (Cross-Site Request Forgery)
- استخدم Flask-WTF للحماية من CSRF
- تحقق من origin headers في طلبات AJAX

### CORS
```python
CORS(app, 
     origins=["https://yourdomain.com"],  # حدد النطاقات المسموحة
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE"])
```

## 6. HTTPS

### في الإنتاج
- استخدم HTTPS دائمًا
- احصل على شهادة SSL مجانية من Let's Encrypt
- أعد توجيه HTTP إلى HTTPS

```nginx
# Nginx configuration
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... باقي الإعدادات
}
```

## 7. المتغيرات البيئية

### لا تكشف عن المعلومات الحساسة
```python
# ✅ آمن
SECRET_KEY = os.getenv('SECRET_KEY')

# ❌ غير آمن
SECRET_KEY = 'my-secret-key-123'
```

### احمِ ملف .env
```bash
# في .gitignore
.env
.env.local
.env.*.local
```

## 8. التسجيل والمراقبة

### تسجيل الأحداث الأمنية
```python
import logging

logging.basicConfig(
    filename='security.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# سجل محاولات تسجيل الدخول الفاشلة
logging.warning(f'Failed login attempt for user: {username} from IP: {ip_address}')
```

### راقب
- محاولات تسجيل الدخول الفاشلة
- الوصول غير المصرح به
- تغييرات البيانات الحساسة
- أخطاء النظام غير المتوقعة

## 9. التحديثات

### حافظ على التحديث
```bash
# تحديث المتطلبات بانتظام
pip list --outdated
pip install --upgrade -r requirements.txt
```

### راجع التحديثات الأمنية
- راقب الثغرات الأمنية في الحزم المستخدمة
- اشترك في تنبيهات الأمان من GitHub
- راجع CVE databases

## 10. النسخ الاحتياطية والاستعادة

### خطة النسخ الاحتياطي
1. نسخ احتياطي يومي لقاعدة البيانات
2. نسخ احتياطي أسبوعي للملفات المرفوعة
3. نسخ احتياطي شهري كامل للنظام

### اختبر الاستعادة
- اختبر استعادة النسخة الاحتياطية شهريًا
- وثق عملية الاستعادة
- تأكد من إمكانية الوصول إلى النسخ الاحتياطية

## 11. الامتثال للوائح

### حماية البيانات الشخصية
- احصل على موافقة المستخدمين
- اسمح بحذف البيانات
- شفّر البيانات الحساسة
- التزم بقوانين حماية البيانات المحلية

### بيانات الأطفال
- احتفظ ببيانات الأطفال بسرية تامة
- قيّد الوصول للموظفين المصرح لهم فقط
- احذف البيانات بعد المدة القانونية

## 12. قائمة المراجعة الأمنية

### قبل الإطلاق
- [ ] تم تعيين SECRET_KEY و JWT_SECRET_KEY قويين
- [ ] تم تعطيل DEBUG في الإنتاج
- [ ] تم إعداد HTTPS
- [ ] تم إعداد جدار الحماية
- [ ] تم تقييد الوصول لقاعدة البيانات
- [ ] تم إعداد النسخ الاحتياطي الآلي
- [ ] تم مراجعة أذونات الملفات
- [ ] تم تحديث جميع المكتبات
- [ ] تم اختبار استعادة النسخة الاحتياطية
- [ ] تم إعداد المراقبة والتنبيهات

### بعد الإطلاق
- [ ] مراقبة السجلات يوميًا
- [ ] تحديث المكتبات شهريًا
- [ ] مراجعة الأمان ربع سنوية
- [ ] تدريب الموظفين على الأمان
- [ ] اختبار الاختراق سنويًا

## الموارد

### روابط مفيدة
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## التواصل

للإبلاغ عن ثغرات أمنية، يرجى التواصل عبر:
- البريد الإلكتروني: security@example.com
- عدم الكشف عن الثغرات علنًا حتى يتم إصلاحها

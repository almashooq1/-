# دليل النشر

## النشر على خادم الإنتاج

### المتطلبات
- Ubuntu 20.04 أو أحدث
- Python 3.8+
- PostgreSQL 12+
- Nginx
- Supervisor (لإدارة العمليات)

### الخطوات

#### 1. تحديث النظام
```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. تثبيت المتطلبات
```bash
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib supervisor -y
```

#### 3. إعداد قاعدة البيانات
```bash
sudo -u postgres psql
```

في PostgreSQL:
```sql
CREATE DATABASE alawael_daycare;
CREATE USER alawael_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE alawael_daycare TO alawael_user;
\q
```

#### 4. إنشاء مستخدم النظام
```bash
sudo useradd -m -s /bin/bash alawael
sudo su - alawael
```

#### 5. استنساخ المشروع
```bash
cd /home/alawael
git clone https://github.com/almashooq1/-.git app
cd app
```

#### 6. إعداد البيئة الافتراضية
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

#### 7. إعداد المتغيرات البيئية
```bash
cp .env.example .env
nano .env
```

تحديث القيم:
```env
DATABASE_URI=postgresql://alawael_user:strong_password_here@localhost/alawael_daycare
SECRET_KEY=generate-strong-secret-key-here
JWT_SECRET_KEY=generate-strong-jwt-secret-key-here
FLASK_ENV=production
DEBUG=False
```

#### 8. تهيئة قاعدة البيانات
```bash
python -c "from 'ملف موقع الاوائل 2' import app, db; app.app_context().push(); db.create_all()"
```

#### 9. إعداد Gunicorn
خروج من المستخدم alawael:
```bash
exit
```

إنشاء ملف Supervisor:
```bash
sudo nano /etc/supervisor/conf.d/alawael.conf
```

محتوى الملف:
```ini
[program:alawael]
directory=/home/alawael/app
command=/home/alawael/app/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 "ملف موقع الاوائل 2:app"
user=alawael
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/alawael/err.log
stdout_logfile=/var/log/alawael/out.log
```

إنشاء مجلد السجلات:
```bash
sudo mkdir -p /var/log/alawael
sudo chown alawael:alawael /var/log/alawael
```

تحديث Supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start alawael
```

#### 10. إعداد Nginx
```bash
sudo nano /etc/nginx/sites-available/alawael
```

محتوى الملف:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/alawael/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /home/alawael/app/static/uploads;
        expires 30d;
    }

    client_max_body_size 16M;
}
```

تفعيل الموقع:
```bash
sudo ln -s /etc/nginx/sites-available/alawael /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 11. إعداد SSL (اختياري ولكن موصى به)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### 12. إعداد جدار الحماية
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## الصيانة

### تحديث التطبيق
```bash
sudo su - alawael
cd app
git pull
source venv/bin/activate
pip install -r requirements.txt
exit
sudo supervisorctl restart alawael
```

### عرض السجلات
```bash
sudo tail -f /var/log/alawael/out.log
sudo tail -f /var/log/alawael/err.log
```

### إعادة تشغيل الخدمة
```bash
sudo supervisorctl restart alawael
```

### النسخ الاحتياطي لقاعدة البيانات
```bash
pg_dump -U alawael_user alawael_daycare > backup_$(date +%Y%m%d_%H%M%S).sql
```

### استعادة النسخة الاحتياطية
```bash
psql -U alawael_user alawael_daycare < backup_file.sql
```

## استكشاف الأخطاء

### التطبيق لا يعمل
```bash
sudo supervisorctl status alawael
sudo supervisorctl restart alawael
```

### خطأ في قاعدة البيانات
- تحقق من صحة بيانات الاتصال في `.env`
- تأكد من تشغيل PostgreSQL: `sudo systemctl status postgresql`

### خطأ 502 Bad Gateway
- تحقق من تشغيل Gunicorn: `sudo supervisorctl status alawael`
- راجع السجلات: `sudo tail -f /var/log/alawael/err.log`

## الأمان

### توصيات الأمان
1. استخدم كلمات مرور قوية
2. حدث النظام بانتظام
3. استخدم HTTPS دائماً
4. قم بنسخ احتياطي منتظم لقاعدة البيانات
5. راقب السجلات بانتظام
6. قيّد وصول SSH
7. استخدم مفاتيح SSH بدلاً من كلمات المرور

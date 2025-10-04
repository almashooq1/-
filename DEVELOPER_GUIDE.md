# دليل التطوير - Developer Guide

## مقدمة
هذا الدليل موجه للمطورين الذين يرغبون في المساهمة في تطوير نظام مراكز الأوائل أو فهم بنيته التقنية.

## إعداد بيئة التطوير

### المتطلبات
- Python 3.8 أو أحدث
- pip (مدير حزم Python)
- Git
- محرر نصوص (VS Code, PyCharm, إلخ)
- PostgreSQL (للتطوير المحلي - اختياري)

### الإعداد الأولي

#### 1. استنساخ المستودع
```bash
git clone https://github.com/almashooq1/-.git
cd -
```

#### 2. إنشاء البيئة الافتراضية
```bash
# على Linux/Mac
python3 -m venv venv
source venv/bin/activate

# على Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. تثبيت المتطلبات
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. إعداد المتغيرات البيئية
```bash
cp .env.example .env
# قم بتحرير .env وتعيين القيم المناسبة
```

#### 5. تهيئة قاعدة البيانات
```bash
python run.py
# أو
python seed_data.py
```

## هيكل المشروع

```
├── static/                 # الملفات الثابتة
│   ├── css/               # ملفات التنسيق
│   ├── js/                # ملفات JavaScript
│   ├── images/            # الصور
│   └── uploads/           # الملفات المرفوعة
├── templates/             # قوالب HTML
├── logs/                  # ملفات السجلات
├── config.py              # إعدادات التطبيق
├── logging_config.py      # إعدادات التسجيل
├── utils.py               # الأدوات المساعدة
├── validators.py          # التحقق من البيانات
├── error_handlers.py      # معالجة الأخطاء
├── database_helpers.py    # مساعدات قاعدة البيانات
├── seed_data.py           # بيانات البداية
├── run.py                 # ملف التشغيل
├── requirements.txt       # متطلبات Python
├── .env.example           # مثال للمتغيرات البيئية
├── .gitignore            # ملفات مستبعدة من Git
├── Dockerfile            # ملف Docker
├── docker-compose.yml    # إعدادات Docker Compose
└── README.md             # الوثائق الرئيسية
```

## معايير الكود

### Python Style Guide
نتبع [PEP 8](https://pep8.org/) مع بعض التعديلات:

```python
# ✅ صحيح
def get_student_by_id(student_id):
    """Get student by ID"""
    student = Student.query.get(student_id)
    return student

# ❌ خطأ
def getStudentById(studentId):
    student=Student.query.get(studentId)
    return student
```

### تسمية المتغيرات
```python
# الثوابت
MAX_FILE_SIZE = 16 * 1024 * 1024

# المتغيرات والدوال
student_name = "أحمد"
def calculate_age(birth_date):
    pass

# الكلاسات
class StudentService:
    pass
```

### التعليقات والوثائق
```python
def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, raises ValidationError otherwise
        
    Raises:
        ValidationError: If email format is invalid
    """
    # Implementation
    pass
```

## أنماط التطوير

### 1. إنشاء Route جديد

```python
@app.route('/api/resource', methods=['GET', 'POST'])
@jwt_required()
def handle_resource():
    if request.method == 'GET':
        # معالجة GET
        items = Resource.query.all()
        return jsonify({
            'success': True,
            'items': [serialize_model(item) for item in items]
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # التحقق من البيانات
            validate_resource_data(data)
            
            # إنشاء المورد
            resource = Resource(**data)
            db.session.add(resource)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'تم الإنشاء بنجاح',
                'id': resource.id
            }), 201
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'حدث خطأ'
            }), 500
```

### 2. إنشاء Model جديد

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class NewModel(db.Model):
    __tablename__ = 'new_model'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # علاقات
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='new_models')
    
    def __repr__(self):
        return f'<NewModel {self.name}>'
```

### 3. إنشاء Validator جديد

```python
def validate_custom_field(value, field_name="الحقل"):
    """Validate custom field"""
    if not value:
        raise ValidationError(f"{field_name} مطلوب")
    
    # منطق التحقق
    if len(value) < 3:
        raise ValidationError(f"{field_name} يجب أن يكون 3 أحرف على الأقل")
    
    return True
```

### 4. استخدام Database Helpers

```python
from database_helpers import serialize_model, paginate_results

# تحويل Model إلى JSON
student_dict = serialize_model(student, exclude=['password'])

# الترقيم
page = request.args.get('page', 1, type=int)
students = Student.query.filter_by(is_active=True)
result = paginate_results(students, page=page, per_page=10)
```

## اختبار الكود

### إنشاء اختبار جديد
```python
import unittest
from app import app, db

class TestStudentAPI(unittest.TestCase):
    def setUp(self):
        """Setup test client"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Cleanup after test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_students(self):
        """Test getting students list"""
        response = self.client.get('/api/students')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
```

### تشغيل الاختبارات
```bash
# تشغيل جميع الاختبارات
python -m unittest discover

# تشغيل اختبار محدد
python -m unittest tests.test_students
```

## التعامل مع قاعدة البيانات

### إنشاء Migration
```bash
flask db init                    # أول مرة فقط
flask db migrate -m "Add new table"  # إنشاء migration
flask db upgrade                 # تطبيق التغييرات
```

### استعلامات شائعة
```python
# البحث
students = Student.query.filter_by(is_active=True).all()

# مع علاقات
student = Student.query.join(Classroom).filter(
    Classroom.name == 'الفصل الأول'
).first()

# الترتيب
students = Student.query.order_by(Student.name).all()

# الترقيم
students = Student.query.paginate(page=1, per_page=10)

# العد
count = Student.query.filter_by(is_active=True).count()

# التجميع
from sqlalchemy import func
stats = db.session.query(
    Classroom.name,
    func.count(Student.id)
).join(Student).group_by(Classroom.name).all()
```

## التصحيح (Debugging)

### استخدام Flask Debug Toolbar
```python
# في ملف الإعداد
if app.config['DEBUG']:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)
```

### تسجيل الأخطاء
```python
# استخدام logger
app.logger.debug('رسالة تصحيح')
app.logger.info('رسالة معلومات')
app.logger.warning('تحذير')
app.logger.error('خطأ')

# في try/except
try:
    # code
except Exception as e:
    app.logger.error(f'Error: {e}', exc_info=True)
```

### Python Debugger
```python
# إضافة نقطة توقف
import pdb; pdb.set_trace()

# أو باستخدام breakpoint (Python 3.7+)
breakpoint()
```

## أدوات مفيدة

### Code Formatting
```bash
# تثبيت
pip install black

# استخدام
black .
```

### Linting
```bash
# تثبيت
pip install flake8

# استخدام
flake8 .
```

### Type Checking
```bash
# تثبيت
pip install mypy

# استخدام
mypy .
```

## Git Workflow

### الفروع
```bash
# إنشاء فرع جديد
git checkout -b feature/اسم-الميزة

# التبديل بين الفروع
git checkout main

# دمج فرع
git merge feature/اسم-الميزة
```

### Commits
```bash
# إضافة ملفات
git add .

# Commit
git commit -m "وصف واضح للتغيير"

# Push
git push origin feature/اسم-الميزة
```

## نشر التطبيق

### باستخدام Docker
```bash
# بناء الصورة
docker build -t alawael-app .

# تشغيل Container
docker run -p 5000:5000 alawael-app

# باستخدام Docker Compose
docker-compose up -d
```

### على خادم Linux
راجع ملف [DEPLOYMENT.md](DEPLOYMENT.md)

## الموارد المفيدة

### الوثائق
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)

### الأدوات
- [Postman](https://www.postman.com/) - اختبار APIs
- [DB Browser for SQLite](https://sqlitebrowser.org/) - تصفح قاعدة البيانات
- [pgAdmin](https://www.pgadmin.org/) - إدارة PostgreSQL

### المجتمع
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flask)
- [Flask Discord](https://discord.gg/pallets)
- [Reddit r/flask](https://reddit.com/r/flask)

## الحصول على المساعدة

إذا واجهت مشكلة:
1. راجع الوثائق
2. ابحث في Issues الموجودة
3. افتح Issue جديد مع وصف تفصيلي للمشكلة

## الخلاصة

هذا الدليل يغطي الأساسيات. للمزيد من التفاصيل:
- راجع الكود المصدري
- اقرأ التعليقات في الملفات
- جرب وتعلم!

نتطلع لمساهماتك! 🚀

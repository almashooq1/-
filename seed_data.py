"""
إنشاء بيانات تجريبية للنظام
Seed Demo Data
"""
import sys
import os
from datetime import datetime, timedelta
import random
from faker import Faker

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import bcrypt
    from config import get_config
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Initialize Faker for Arabic data
fake = Faker('ar_SA')

# Arabic names lists
MALE_NAMES = [
    "محمد", "أحمد", "علي", "حسن", "حسين", "عبدالله", "عبدالرحمن", "خالد",
    "سعيد", "سلمان", "فيصل", "عمر", "يوسف", "إبراهيم", "عبدالعزيز"
]

FEMALE_NAMES = [
    "فاطمة", "عائشة", "زينب", "مريم", "نورة", "سارة", "ليلى", "رقية",
    "خديجة", "هند", "منى", "ريم", "شهد", "جود", "لين"
]

FAMILY_NAMES = [
    "الأحمد", "العلي", "الحسن", "العمر", "السعيد", "الخالد", "المحمد",
    "الفيصل", "السلمان", "العبدالله", "الإبراهيم", "اليوسف"
]


def create_demo_data():
    """إنشاء بيانات تجريبية"""
    
    # Initialize Flask app
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)
    
    # Initialize database
    db = SQLAlchemy(app)
    
    # Import models (simplified versions)
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        email = db.Column(db.String(120), unique=True)
        national_id = db.Column(db.String(20), unique=True)
        password = db.Column(db.String(255))
        role = db.Column(db.String(20))
        phone = db.Column(db.String(20))
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class AcademicYear(db.Model):
        __tablename__ = 'academic_years'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        start_date = db.Column(db.Date)
        end_date = db.Column(db.Date)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class Classroom(db.Model):
        __tablename__ = 'classrooms'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        level = db.Column(db.String(50))
        capacity = db.Column(db.Integer)
        academic_year_id = db.Column(db.Integer)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class Student(db.Model):
        __tablename__ = 'students'
        id = db.Column(db.Integer, primary_key=True)
        national_id = db.Column(db.String(20), unique=True)
        name = db.Column(db.String(100))
        birth_date = db.Column(db.Date)
        gender = db.Column(db.String(10))
        guardian_name = db.Column(db.String(100))
        guardian_phone = db.Column(db.String(20))
        guardian_email = db.Column(db.String(120))
        classroom_id = db.Column(db.Integer)
        academic_year_id = db.Column(db.Integer)
        enrollment_date = db.Column(db.Date, default=datetime.utcnow)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    with app.app_context():
        try:
            print("\n🚀 بدء إنشاء البيانات التجريبية...\n")
            
            # 1. Create Academic Year
            print("1️⃣  إنشاء السنة الدراسية...")
            year = AcademicYear.query.filter_by(is_active=True).first()
            if not year:
                year = AcademicYear(
                    name="السنة الدراسية 2024/2025",
                    start_date=datetime(2024, 9, 1).date(),
                    end_date=datetime(2025, 6, 30).date(),
                    is_active=True
                )
                db.session.add(year)
                db.session.flush()
                print("   ✅ تم إنشاء السنة الدراسية")
            else:
                print(f"   ℹ️  السنة الدراسية موجودة: {year.name}")
            
            # 2. Create Classrooms
            print("\n2️⃣  إنشاء الفصول الدراسية...")
            classroom_names = [
                ("الفصل الأول", "تمهيدي"),
                ("الفصل الثاني", "تمهيدي"),
                ("الفصل الثالث", "مبتدئ"),
                ("الفصل الرابع", "مبتدئ"),
                ("الفصل الخامس", "متوسط"),
                ("الفصل السادس", "متوسط"),
                ("الفصل السابع", "متقدم"),
                ("الفصل الثامن", "متقدم"),
                ("الفصل التاسع", "متخصص"),
                ("الفصل العاشر", "متخصص"),
            ]
            
            classrooms = []
            for name, level in classroom_names:
                classroom = Classroom.query.filter_by(name=name, academic_year_id=year.id).first()
                if not classroom:
                    classroom = Classroom(
                        name=name,
                        level=level,
                        capacity=random.randint(8, 15),
                        academic_year_id=year.id,
                        is_active=True
                    )
                    db.session.add(classroom)
                    classrooms.append(classroom)
                else:
                    classrooms.append(classroom)
            
            db.session.flush()
            print(f"   ✅ تم إنشاء {len(classroom_names)} فصل دراسي")
            
            # 3. Create Teachers
            print("\n3️⃣  إنشاء المعلمين والأخصائيين...")
            specializations = [
                "علاج طبيعي",
                "علاج وظيفي",
                "علاج نطق ولغة",
                "علاج سلوكي",
                "تربية خاصة",
                "تأهيل حركي",
                "تأهيل معرفي",
                "تأهيل اجتماعي"
            ]
            
            teachers_created = 0
            for i in range(20):
                gender = random.choice(['male', 'female'])
                first_name = random.choice(MALE_NAMES if gender == 'male' else FEMALE_NAMES)
                family_name = random.choice(FAMILY_NAMES)
                name = f"{first_name} {family_name}"
                email = f"teacher{i+1}@alawael.com"
                national_id = f"10{i+1:08d}"
                
                # Check if exists
                if User.query.filter_by(email=email).first():
                    continue
                
                password = bcrypt.hashpw(national_id.encode('utf-8'), bcrypt.gensalt())
                
                teacher = User(
                    name=name,
                    email=email,
                    national_id=national_id,
                    password=password.decode('utf-8'),
                    role='teacher',
                    phone=f"05{random.randint(10000000, 99999999)}",
                    is_active=True
                )
                db.session.add(teacher)
                teachers_created += 1
            
            db.session.flush()
            print(f"   ✅ تم إنشاء {teachers_created} معلم/أخصائي")
            
            # 4. Create Students
            print("\n4️⃣  إنشاء الطلاب...")
            students_created = 0
            for i in range(50):
                gender = random.choice(['male', 'female'])
                first_name = random.choice(MALE_NAMES if gender == 'male' else FEMALE_NAMES)
                father_name = random.choice(MALE_NAMES)
                family_name = random.choice(FAMILY_NAMES)
                name = f"{first_name} {father_name} {family_name}"
                
                national_id = f"20{i+1:08d}"
                
                # Check if exists
                if Student.query.filter_by(national_id=national_id).first():
                    continue
                
                # Random birth date (4-12 years old)
                age_years = random.randint(4, 12)
                birth_date = datetime.now() - timedelta(days=age_years*365 + random.randint(0, 364))
                
                # Random guardian
                guardian_gender = random.choice(['male', 'female'])
                guardian_first = random.choice(MALE_NAMES if guardian_gender == 'male' else FEMALE_NAMES)
                guardian_name = f"{guardian_first} {family_name}"
                
                student = Student(
                    national_id=national_id,
                    name=name,
                    birth_date=birth_date.date(),
                    gender=gender,
                    guardian_name=guardian_name,
                    guardian_phone=f"05{random.randint(10000000, 99999999)}",
                    guardian_email=f"parent{i+1}@example.com",
                    classroom_id=random.choice(classrooms).id,
                    academic_year_id=year.id,
                    enrollment_date=(datetime.now() - timedelta(days=random.randint(30, 180))).date(),
                    is_active=True
                )
                db.session.add(student)
                students_created += 1
            
            db.session.commit()
            print(f"   ✅ تم إنشاء {students_created} طالب")
            
            # Summary
            print("\n" + "="*60)
            print("✅ تم إنشاء البيانات التجريبية بنجاح!")
            print("="*60)
            print(f"\n📊 الإحصائيات:")
            print(f"   • سنة دراسية: 1")
            print(f"   • فصول: {len(classroom_names)}")
            print(f"   • معلمون: {teachers_created}")
            print(f"   • طلاب: {students_created}")
            print("\n💡 معلومات تسجيل الدخول للمعلمين:")
            print("   البريد الإلكتروني: teacher1@alawael.com (إلى teacher20@alawael.com)")
            print("   كلمة المرور: رقم الهوية الخاص بكل معلم")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n❌ حدث خطأ: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("   نظام ERP - إنشاء بيانات تجريبية")
    print("   مراكز الأوائل للرعاية النهارية 2")
    print("="*60 + "\n")
    
    response = input("⚠️  هذا سيُنشئ بيانات تجريبية في قاعدة البيانات. هل تريد المتابعة؟ (y/n): ")
    
    if response.lower() == 'y':
        create_demo_data()
    else:
        print("\n❌ تم الإلغاء.")
    
    print("\n" + "="*60)
    print("   شكراً لاستخدام نظام ERP")
    print("="*60 + "\n")

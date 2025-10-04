#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database initialization and seed data script
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, date
import bcrypt


def init_database(app, db):
    """Initialize database with tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully")


def seed_admin_user(app, db, User):
    """Create default admin user"""
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@alawael.com').first()
        
        if not admin:
            print("Creating admin user...")
            
            # Hash password
            password = 'Admin@123'  # Change this in production!
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            admin = User(
                name='المدير العام',
                email='admin@alawael.com',
                national_id='1111111111',
                password=hashed_password.decode('utf-8'),
                role='admin',
                phone='0501234567',
                address='الرياض',
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully")
            print(f"   Email: admin@alawael.com")
            print(f"   Password: {password}")
            print("   ⚠️  تحذير: يرجى تغيير كلمة المرور بعد تسجيل الدخول!")
        else:
            print("ℹ️  Admin user already exists")


def seed_academic_year(app, db, AcademicYear):
    """Create current academic year"""
    with app.app_context():
        # Check if active year exists
        active_year = AcademicYear.query.filter_by(is_active=True).first()
        
        if not active_year:
            print("Creating academic year...")
            
            current_year = datetime.now().year
            year = AcademicYear(
                name=f'العام الدراسي {current_year}-{current_year+1}',
                start_date=date(current_year, 9, 1),
                end_date=date(current_year+1, 6, 30),
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(year)
            db.session.commit()
            
            print("✅ Academic year created successfully")
        else:
            print("ℹ️  Active academic year already exists")


def seed_skill_domains(app, db, SkillDomain):
    """Create default skill domains"""
    with app.app_context():
        domains = [
            {'name': 'المهارات المعرفية', 'description': 'المهارات العقلية والإدراكية', 'order_index': 1},
            {'name': 'المهارات اللغوية', 'description': 'مهارات التواصل واللغة', 'order_index': 2},
            {'name': 'المهارات الحركية', 'description': 'المهارات الحركية الدقيقة والكبيرة', 'order_index': 3},
            {'name': 'المهارات الاجتماعية', 'description': 'مهارات التفاعل الاجتماعي', 'order_index': 4},
            {'name': 'مهارات الرعاية الذاتية', 'description': 'مهارات العناية بالنفس', 'order_index': 5},
        ]
        
        created_count = 0
        for domain_data in domains:
            existing = SkillDomain.query.filter_by(name=domain_data['name']).first()
            if not existing:
                domain = SkillDomain(**domain_data, is_active=True, created_at=datetime.utcnow())
                db.session.add(domain)
                created_count += 1
        
        db.session.commit()
        
        if created_count > 0:
            print(f"✅ Created {created_count} skill domains")
        else:
            print("ℹ️  Skill domains already exist")


def seed_clinic_types(app, db, ClinicType):
    """Create default clinic types"""
    with app.app_context():
        clinics = [
            {
                'clinic_name': 'عيادة النطق واللغة',
                'description': 'تقييم وعلاج اضطرابات النطق واللغة',
                'icon': 'fas fa-comments',
                'color': '#4CAF50'
            },
            {
                'clinic_name': 'عيادة العلاج الطبيعي',
                'description': 'علاج المشاكل الحركية والجسدية',
                'icon': 'fas fa-wheelchair',
                'color': '#2196F3'
            },
            {
                'clinic_name': 'عيادة العلاج الوظيفي',
                'description': 'تحسين المهارات الحياتية اليومية',
                'icon': 'fas fa-hand-holding-heart',
                'color': '#FF9800'
            },
            {
                'clinic_name': 'عيادة التربية الخاصة',
                'description': 'برامج تعليمية متخصصة',
                'icon': 'fas fa-graduation-cap',
                'color': '#9C27B0'
            },
            {
                'clinic_name': 'عيادة الإرشاد النفسي',
                'description': 'الدعم النفسي والإرشاد الأسري',
                'icon': 'fas fa-brain',
                'color': '#E91E63'
            }
        ]
        
        created_count = 0
        for clinic_data in clinics:
            existing = ClinicType.query.filter_by(clinic_name=clinic_data['clinic_name']).first()
            if not existing:
                clinic = ClinicType(**clinic_data, is_active=True, created_at=datetime.utcnow())
                db.session.add(clinic)
                created_count += 1
        
        db.session.commit()
        
        if created_count > 0:
            print(f"✅ Created {created_count} clinic types")
        else:
            print("ℹ️  Clinic types already exist")


def run_seeds(app, db):
    """Run all seed functions"""
    print("=" * 50)
    print("تهيئة قاعدة البيانات")
    print("Database Initialization")
    print("=" * 50)
    print()
    
    # Import models
    try:
        from models import User, AcademicYear, SkillDomain, ClinicType
        
        # Initialize database
        init_database(app, db)
        
        # Seed data
        seed_admin_user(app, db, User)
        seed_academic_year(app, db, AcademicYear)
        seed_skill_domains(app, db, SkillDomain)
        seed_clinic_types(app, db, ClinicType)
        
        print()
        print("=" * 50)
        print("✅ تم إكمال التهيئة بنجاح!")
        print("✅ Initialization completed successfully!")
        print("=" * 50)
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد النماذج: {e}")
        print("يرجى التأكد من وجود ملف models.py")
    except Exception as e:
        print(f"❌ خطأ: {e}")


if __name__ == '__main__':
    print("يرجى تشغيل هذا السكريبت من التطبيق الرئيسي")
    print("Please run this script from the main application")

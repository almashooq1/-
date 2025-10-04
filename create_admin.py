"""
إنشاء مستخدم مدير النظام
Create Admin User
"""
import sys
import os
from datetime import datetime

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


def create_admin_user():
    """إنشاء مستخدم مدير"""
    
    # Initialize Flask app
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)
    
    # Initialize database
    db = SQLAlchemy(app)
    
    # Define User model (simplified)
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        national_id = db.Column(db.String(20), unique=True, nullable=False)
        password = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(20), default='user')
        phone = db.Column(db.String(20))
        address = db.Column(db.Text)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    with app.app_context():
        try:
            # Check if admin exists
            admin = User.query.filter_by(email='admin@alawael.com').first()
            
            if admin:
                print("⚠️  المستخدم المدير موجود بالفعل!")
                print(f"   البريد الإلكتروني: admin@alawael.com")
                
                # Ask if want to reset password
                response = input("\nهل تريد إعادة تعيين كلمة المرور؟ (y/n): ")
                if response.lower() != 'y':
                    return
                
                # Reset password
                new_password = input("أدخل كلمة المرور الجديدة: ")
                if not new_password:
                    print("❌ كلمة المرور لا يمكن أن تكون فارغة!")
                    return
                
                hashed_password = bcrypt.hashpw(
                    new_password.encode('utf-8'),
                    bcrypt.gensalt()
                )
                admin.password = hashed_password.decode('utf-8')
                db.session.commit()
                print("✅ تم إعادة تعيين كلمة المرور بنجاح!")
                
            else:
                # Create new admin
                print("\n=== إنشاء مستخدم مدير جديد ===\n")
                
                # Get admin details
                name = input("الاسم الكامل [مدير النظام]: ").strip() or "مدير النظام"
                email = input("البريد الإلكتروني [admin@alawael.com]: ").strip() or "admin@alawael.com"
                national_id = input("رقم الهوية [1000000001]: ").strip() or "1000000001"
                password = input("كلمة المرور [Admin@2024]: ").strip() or "Admin@2024"
                phone = input("رقم الجوال [0500000000]: ").strip() or "0500000000"
                
                # Validate email
                if User.query.filter_by(email=email).first():
                    print(f"❌ البريد الإلكتروني {email} مستخدم بالفعل!")
                    return
                
                # Validate national ID
                if User.query.filter_by(national_id=national_id).first():
                    print(f"❌ رقم الهوية {national_id} مسجل بالفعل!")
                    return
                
                # Hash password
                hashed_password = bcrypt.hashpw(
                    password.encode('utf-8'),
                    bcrypt.gensalt()
                )
                
                # Create admin user
                admin = User(
                    name=name,
                    email=email,
                    national_id=national_id,
                    password=hashed_password.decode('utf-8'),
                    role='admin',
                    phone=phone,
                    address='مراكز الأوائل للرعاية النهارية',
                    is_active=True
                )
                
                db.session.add(admin)
                db.session.commit()
                
                print("\n" + "="*50)
                print("✅ تم إنشاء مستخدم المدير بنجاح!")
                print("="*50)
                print(f"\nمعلومات تسجيل الدخول:")
                print(f"   البريد الإلكتروني: {email}")
                print(f"   كلمة المرور: {password}")
                print(f"   الدور: مدير النظام (Admin)")
                print("\n⚠️  تأكد من تغيير كلمة المرور بعد أول تسجيل دخول!")
                print("="*50)
                
        except Exception as e:
            print(f"❌ حدث خطأ: {e}")
            db.session.rollback()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("   نظام ERP - إنشاء مستخدم مدير")
    print("   مراكز الأوائل للرعاية النهارية 2")
    print("="*50 + "\n")
    
    create_admin_user()
    
    print("\n" + "="*50)
    print("   شكراً لاستخدام نظام ERP")
    print("="*50 + "\n")

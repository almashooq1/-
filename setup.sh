#!/bin/bash

# نص التثبيت السريع لنظام مراكز الأوائل
# Quick Setup Script for Al-Awael Daycare System

echo "=========================================="
echo "مرحباً بك في نظام مراكز الأوائل للرعاية النهارية"
echo "Welcome to Al-Awael Daycare System"
echo "=========================================="
echo ""

# التحقق من Python
echo "🔍 التحقق من تثبيت Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3.8 أو أحدث."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ تم العثور على Python $PYTHON_VERSION"
echo ""

# إنشاء البيئة الافتراضية
echo "📦 إنشاء البيئة الافتراضية..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ تم إنشاء البيئة الافتراضية"
else
    echo "ℹ️  البيئة الافتراضية موجودة بالفعل"
fi
echo ""

# تفعيل البيئة الافتراضية
echo "🔄 تفعيل البيئة الافتراضية..."
source venv/bin/activate
echo "✅ تم تفعيل البيئة الافتراضية"
echo ""

# تحديث pip
echo "⬆️  تحديث pip..."
pip install --upgrade pip --quiet
echo "✅ تم تحديث pip"
echo ""

# تثبيت المتطلبات
echo "📥 تثبيت المتطلبات..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo "✅ تم تثبيت جميع المتطلبات"
else
    echo "❌ ملف requirements.txt غير موجود"
    exit 1
fi
echo ""

# نسخ ملف البيئة
echo "⚙️  إعداد ملف البيئة..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ تم نسخ ملف .env من .env.example"
        echo "⚠️  تحذير: يرجى تحديث القيم في ملف .env"
    else
        echo "⚠️  ملف .env.example غير موجود"
    fi
else
    echo "ℹ️  ملف .env موجود بالفعل"
fi
echo ""

# إنشاء المجلدات الضرورية
echo "📁 إنشاء المجلدات الضرورية..."
mkdir -p static/uploads/students
mkdir -p static/uploads/teachers
mkdir -p static/images
echo "✅ تم إنشاء المجلدات"
echo ""

# تهيئة قاعدة البيانات
echo "🗄️  تهيئة قاعدة البيانات..."
python3 -c "from 'ملف موقع الاوائل 2' import app, db; app.app_context().push(); db.create_all()" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ تم تهيئة قاعدة البيانات"
else
    echo "⚠️  تحذير: قد تكون هناك مشكلة في تهيئة قاعدة البيانات"
fi
echo ""

# إنهاء
echo "=========================================="
echo "✨ تم إكمال الإعداد بنجاح!"
echo "=========================================="
echo ""
echo "للبدء، قم بتشغيل:"
echo "  source venv/bin/activate"
echo "  python3 'ملف موقع الاوائل 2.py'"
echo ""
echo "ثم افتح المتصفح على:"
echo "  http://localhost:5000"
echo ""
echo "=========================================="

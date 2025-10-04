@echo off
REM نص التثبيت السريع لنظام مراكز الأوائل (Windows)
REM Quick Setup Script for Al-Awael Daycare System (Windows)

echo ==========================================
echo مرحباً بك في نظام مراكز الأوائل للرعاية النهارية
echo Welcome to Al-Awael Daycare System
echo ==========================================
echo.

REM التحقق من Python
echo 🔍 التحقق من تثبيت Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت. يرجى تثبيت Python 3.8 أو أحدث.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ تم العثور على Python %PYTHON_VERSION%
echo.

REM إنشاء البيئة الافتراضية
echo 📦 إنشاء البيئة الافتراضية...
if not exist "venv" (
    python -m venv venv
    echo ✅ تم إنشاء البيئة الافتراضية
) else (
    echo ℹ️  البيئة الافتراضية موجودة بالفعل
)
echo.

REM تفعيل البيئة الافتراضية
echo 🔄 تفعيل البيئة الافتراضية...
call venv\Scripts\activate.bat
echo ✅ تم تفعيل البيئة الافتراضية
echo.

REM تحديث pip
echo ⬆️  تحديث pip...
python -m pip install --upgrade pip --quiet
echo ✅ تم تحديث pip
echo.

REM تثبيت المتطلبات
echo 📥 تثبيت المتطلبات...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    echo ✅ تم تثبيت جميع المتطلبات
) else (
    echo ❌ ملف requirements.txt غير موجود
    pause
    exit /b 1
)
echo.

REM نسخ ملف البيئة
echo ⚙️  إعداد ملف البيئة...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✅ تم نسخ ملف .env من .env.example
        echo ⚠️  تحذير: يرجى تحديث القيم في ملف .env
    ) else (
        echo ⚠️  ملف .env.example غير موجود
    )
) else (
    echo ℹ️  ملف .env موجود بالفعل
)
echo.

REM إنشاء المجلدات الضرورية
echo 📁 إنشاء المجلدات الضرورية...
if not exist "static\uploads\students" mkdir static\uploads\students
if not exist "static\uploads\teachers" mkdir static\uploads\teachers
if not exist "static\images" mkdir static\images
echo ✅ تم إنشاء المجلدات
echo.

REM تهيئة قاعدة البيانات
echo 🗄️  تهيئة قاعدة البيانات...
python -c "from 'ملف موقع الاوائل 2' import app, db; app.app_context().push(); db.create_all()" 2>nul
if %errorlevel% equ 0 (
    echo ✅ تم تهيئة قاعدة البيانات
) else (
    echo ⚠️  تحذير: قد تكون هناك مشكلة في تهيئة قاعدة البيانات
)
echo.

REM إنهاء
echo ==========================================
echo ✨ تم إكمال الإعداد بنجاح!
echo ==========================================
echo.
echo للبدء، قم بتشغيل:
echo   venv\Scripts\activate.bat
echo   python "ملف موقع الاوائل 2.py"
echo.
echo ثم افتح المتصفح على:
echo   http://localhost:5000
echo.
echo ==========================================
pause

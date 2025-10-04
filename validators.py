# Validation Functions

import re
from datetime import datetime, date


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_required(value, field_name):
    """Validate that a field is not empty"""
    if value is None or (isinstance(value, str) and value.strip() == ''):
        raise ValidationError(f"{field_name} مطلوب")
    return True


def validate_email(email):
    """Validate email format"""
    if not email:
        raise ValidationError("البريد الإلكتروني مطلوب")
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError("البريد الإلكتروني غير صحيح")
    
    return True


def validate_national_id(national_id):
    """Validate Saudi national ID"""
    if not national_id:
        raise ValidationError("رقم الهوية مطلوب")
    
    # Remove spaces
    national_id = national_id.replace(' ', '')
    
    # Check length
    if len(national_id) != 10:
        raise ValidationError("رقم الهوية يجب أن يكون 10 أرقام")
    
    # Check if all characters are digits
    if not national_id.isdigit():
        raise ValidationError("رقم الهوية يجب أن يحتوي على أرقام فقط")
    
    # Check first digit (1 for Saudi, 2 for resident)
    if national_id[0] not in ['1', '2']:
        raise ValidationError("رقم الهوية غير صحيح")
    
    return True


def validate_phone(phone):
    """Validate Saudi phone number"""
    if not phone:
        raise ValidationError("رقم الجوال مطلوب")
    
    # Remove spaces and special characters
    phone = re.sub(r'[^\d]', '', phone)
    
    # Check length and format
    if len(phone) == 10 and phone.startswith('05'):
        return True
    elif len(phone) == 9 and phone.startswith('5'):
        return True
    else:
        raise ValidationError("رقم الجوال غير صحيح (يجب أن يبدأ بـ 05)")


def validate_date(date_str, field_name="التاريخ"):
    """Validate date format"""
    if not date_str:
        raise ValidationError(f"{field_name} مطلوب")
    
    try:
        if isinstance(date_str, str):
            datetime.strptime(date_str, '%Y-%m-%d')
        elif not isinstance(date_str, (date, datetime)):
            raise ValidationError(f"{field_name} غير صحيح")
    except ValueError:
        raise ValidationError(f"{field_name} يجب أن يكون بصيغة YYYY-MM-DD")
    
    return True


def validate_birth_date(birth_date):
    """Validate birth date (must be in the past)"""
    validate_date(birth_date, "تاريخ الميلاد")
    
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    if birth_date >= date.today():
        raise ValidationError("تاريخ الميلاد يجب أن يكون في الماضي")
    
    return True


def validate_password(password):
    """Validate password strength"""
    if not password:
        raise ValidationError("كلمة المرور مطلوبة")
    
    if len(password) < 8:
        raise ValidationError("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValidationError("كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل")
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise ValidationError("كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل")
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        raise ValidationError("كلمة المرور يجب أن تحتوي على رقم واحد على الأقل")
    
    return True


def validate_age_range(birth_date, min_age=0, max_age=18):
    """Validate age is within range"""
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    if age < min_age or age > max_age:
        raise ValidationError(f"العمر يجب أن يكون بين {min_age} و {max_age} سنة")
    
    return True


def validate_positive_number(value, field_name):
    """Validate that a number is positive"""
    try:
        num = float(value)
        if num <= 0:
            raise ValidationError(f"{field_name} يجب أن يكون رقم موجب")
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} يجب أن يكون رقم صحيح")
    
    return True


def validate_integer(value, field_name):
    """Validate that a value is an integer"""
    try:
        int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} يجب أن يكون رقم صحيح")
    
    return True


def validate_choice(value, choices, field_name):
    """Validate that value is in allowed choices"""
    if value not in choices:
        choices_str = ', '.join(str(c) for c in choices)
        raise ValidationError(f"{field_name} يجب أن يكون أحد القيم التالية: {choices_str}")
    
    return True


def validate_string_length(value, min_length=None, max_length=None, field_name="الحقل"):
    """Validate string length"""
    if value is None:
        value = ''
    
    length = len(str(value))
    
    if min_length is not None and length < min_length:
        raise ValidationError(f"{field_name} يجب أن يحتوي على {min_length} حرف على الأقل")
    
    if max_length is not None and length > max_length:
        raise ValidationError(f"{field_name} يجب ألا يتجاوز {max_length} حرف")
    
    return True


def validate_file_size(file, max_size_mb=16):
    """Validate uploaded file size"""
    if file:
        file.seek(0, 2)  # Move to end of file
        size = file.tell()  # Get current position (file size)
        file.seek(0)  # Reset to beginning
        
        max_size_bytes = max_size_mb * 1024 * 1024
        if size > max_size_bytes:
            raise ValidationError(f"حجم الملف يجب ألا يتجاوز {max_size_mb} ميجابايت")
    
    return True


def validate_file_extension(filename, allowed_extensions):
    """Validate file extension"""
    if not filename or '.' not in filename:
        raise ValidationError("امتداد الملف غير صحيح")
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        allowed = ', '.join(allowed_extensions)
        raise ValidationError(f"الامتدادات المسموحة: {allowed}")
    
    return True


def validate_student_data(data):
    """Validate student registration data"""
    errors = []
    
    try:
        validate_required(data.get('name'), 'الاسم')
        validate_string_length(data.get('name'), min_length=2, max_length=100, field_name='الاسم')
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        validate_national_id(data.get('national_id'))
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        if data.get('birth_date'):
            validate_birth_date(data.get('birth_date'))
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        if data.get('guardian_phone'):
            validate_phone(data.get('guardian_phone'))
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        if data.get('guardian_email'):
            validate_email(data.get('guardian_email'))
    except ValidationError as e:
        errors.append(str(e))
    
    if errors:
        raise ValidationError(' | '.join(errors))
    
    return True


def validate_teacher_data(data):
    """Validate teacher registration data"""
    errors = []
    
    try:
        validate_required(data.get('name'), 'الاسم')
        validate_string_length(data.get('name'), min_length=2, max_length=100, field_name='الاسم')
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        validate_national_id(data.get('national_id'))
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        validate_email(data.get('email'))
    except ValidationError as e:
        errors.append(str(e))
    
    try:
        if data.get('phone'):
            validate_phone(data.get('phone'))
    except ValidationError as e:
        errors.append(str(e))
    
    if errors:
        raise ValidationError(' | '.join(errors))
    
    return True

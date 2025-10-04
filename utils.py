# Utility Functions

import os
import secrets
import string
from werkzeug.utils import secure_filename
from datetime import datetime, date
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def generate_random_string(length=32):
    """Generate a random string for tokens, keys, etc."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, folder, allowed_extensions=None):
    """Save uploaded file securely"""
    if not file or file.filename == '':
        return None, "لم يتم اختيار ملف"
    
    if not allowed_file(file.filename, allowed_extensions):
        return None, "نوع الملف غير مسموح"
    
    # Create folder if it doesn't exist
    upload_path = os.path.join('static/uploads', folder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{name}_{timestamp}{ext}"
    
    # Save file
    file_path = os.path.join(upload_path, unique_filename)
    file.save(file_path)
    
    # Return relative path
    return os.path.join(folder, unique_filename), None


def delete_file(file_path):
    """Delete file safely"""
    try:
        full_path = os.path.join('static/uploads', file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception as e:
        print(f"Error deleting file: {e}")
    return False


def format_date(date_obj, format_str='%Y-%m-%d'):
    """Format date object to string"""
    if date_obj is None:
        return None
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime(format_str)


def parse_date(date_str, format_str='%Y-%m-%d'):
    """Parse date string to date object"""
    if date_str is None or date_str == '':
        return None
    if isinstance(date_str, (date, datetime)):
        return date_str
    try:
        return datetime.strptime(date_str, format_str).date()
    except ValueError:
        return None


def calculate_age(birth_date):
    """Calculate age from birth date"""
    if birth_date is None:
        return None
    
    if isinstance(birth_date, str):
        birth_date = parse_date(birth_date)
    
    today = date.today()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if today.month < birth_date.month or \
       (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age


def paginate_query(query, page=1, per_page=10, max_per_page=100):
    """Paginate a SQLAlchemy query"""
    # Validate parameters
    page = max(1, page)
    per_page = min(max(1, per_page), max_per_page)
    
    # Execute pagination
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': pagination.items,
        'pagination': {
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'next_num': pagination.next_num,
            'prev_num': pagination.prev_num
        }
    }


def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if text is None:
        return None
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def get_client_ip():
    """Get client IP address from request"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr


def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        
        # Import here to avoid circular imports
        from models import User
        user = User.query.get(current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({
                'success': False,
                'error': 'يتطلب صلاحيات المدير'
            }), 403
        
        return fn(*args, **kwargs)
    return wrapper


def teacher_or_admin_required(fn):
    """Decorator to require teacher or admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        
        # Import here to avoid circular imports
        from models import User
        user = User.query.get(current_user_id)
        
        if not user or user.role not in ['admin', 'teacher']:
            return jsonify({
                'success': False,
                'error': 'يتطلب صلاحيات المعلم أو المدير'
            }), 403
        
        return fn(*args, **kwargs)
    return wrapper


def validate_national_id(national_id):
    """Validate Saudi national ID format"""
    if not national_id:
        return False
    
    # Remove spaces and special characters
    national_id = ''.join(filter(str.isdigit, national_id))
    
    # Should be 10 digits
    if len(national_id) != 10:
        return False
    
    # Should start with 1 or 2
    if national_id[0] not in ['1', '2']:
        return False
    
    return True


def validate_phone(phone):
    """Validate Saudi phone number format"""
    if not phone:
        return False
    
    # Remove spaces and special characters
    phone = ''.join(filter(str.isdigit, phone))
    
    # Should be 10 digits starting with 05
    if len(phone) == 10 and phone.startswith('05'):
        return True
    
    # Or 9 digits starting with 5
    if len(phone) == 9 and phone.startswith('5'):
        return True
    
    return False


def format_phone(phone):
    """Format phone number to standard format"""
    if not phone:
        return None
    
    # Remove all non-digits
    phone = ''.join(filter(str.isdigit, phone))
    
    # Add leading 0 if needed
    if len(phone) == 9 and phone.startswith('5'):
        phone = '0' + phone
    
    return phone

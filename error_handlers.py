# Error Handlers

from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging


def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        app.logger.warning(f"Bad Request: {error}")
        return jsonify({
            'success': False,
            'error': 'طلب غير صحيح',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors"""
        app.logger.warning(f"Unauthorized access attempt: {error}")
        return jsonify({
            'success': False,
            'error': 'غير مصرح',
            'message': 'يرجى تسجيل الدخول للوصول إلى هذا المورد'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors"""
        app.logger.warning(f"Forbidden access: {error}")
        return jsonify({
            'success': False,
            'error': 'ممنوع',
            'message': 'ليس لديك صلاحية للوصول إلى هذا المورد'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        app.logger.info(f"Resource not found: {error}")
        return jsonify({
            'success': False,
            'error': 'غير موجود',
            'message': 'المورد المطلوب غير موجود'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        app.logger.warning(f"Method not allowed: {error}")
        return jsonify({
            'success': False,
            'error': 'طريقة غير مسموحة',
            'message': 'الطريقة المستخدمة غير مسموحة لهذا المورد'
        }), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle 413 Request Entity Too Large errors"""
        app.logger.warning(f"File too large: {error}")
        return jsonify({
            'success': False,
            'error': 'الملف كبير جداً',
            'message': 'حجم الملف المرفوع يتجاوز الحد المسموح'
        }), 413
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle 422 Unprocessable Entity errors"""
        app.logger.warning(f"Unprocessable entity: {error}")
        return jsonify({
            'success': False,
            'error': 'بيانات غير صحيحة',
            'message': 'لا يمكن معالجة البيانات المرسلة'
        }), 422
    
    @app.errorhandler(429)
    def too_many_requests(error):
        """Handle 429 Too Many Requests errors"""
        app.logger.warning(f"Rate limit exceeded: {error}")
        return jsonify({
            'success': False,
            'error': 'طلبات كثيرة',
            'message': 'تم تجاوز الحد المسموح من الطلبات. يرجى المحاولة لاحقاً'
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        app.logger.error(f"Internal server error: {error}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'خطأ في الخادم',
            'message': 'حدث خطأ غير متوقع. يرجى المحاولة لاحقاً'
        }), 500
    
    @app.errorhandler(502)
    def bad_gateway(error):
        """Handle 502 Bad Gateway errors"""
        app.logger.error(f"Bad gateway: {error}")
        return jsonify({
            'success': False,
            'error': 'خطأ في الاتصال',
            'message': 'حدث خطأ في الاتصال بالخادم'
        }), 502
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable errors"""
        app.logger.error(f"Service unavailable: {error}")
        return jsonify({
            'success': False,
            'error': 'الخدمة غير متاحة',
            'message': 'الخدمة غير متاحة حالياً. يرجى المحاولة لاحقاً'
        }), 503
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle all other unexpected errors"""
        app.logger.error(f"Unexpected error: {error}", exc_info=True)
        
        # If it's an HTTP exception, return its status code
        if isinstance(error, HTTPException):
            return jsonify({
                'success': False,
                'error': error.name,
                'message': error.description
            }), error.code
        
        # For all other exceptions in production, return generic error
        if not app.config.get('DEBUG'):
            return jsonify({
                'success': False,
                'error': 'خطأ غير متوقع',
                'message': 'حدث خطأ غير متوقع. يرجى الاتصال بالدعم الفني'
            }), 500
        
        # In development, return detailed error
        return jsonify({
            'success': False,
            'error': type(error).__name__,
            'message': str(error)
        }), 500
    
    # Custom error for validation errors
    from validators import ValidationError
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle validation errors"""
        app.logger.warning(f"Validation error: {error}")
        return jsonify({
            'success': False,
            'error': 'خطأ في التحقق من البيانات',
            'message': str(error)
        }), 400
    
    # JWT errors
    from flask_jwt_extended.exceptions import JWTExtendedException
    
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(error):
        """Handle JWT errors"""
        app.logger.warning(f"JWT error: {error}")
        return jsonify({
            'success': False,
            'error': 'خطأ في المصادقة',
            'message': 'رمز المصادقة غير صالح أو منتهي الصلاحية'
        }), 401
    
    app.logger.info('Error handlers registered')
    
    return app

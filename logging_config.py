# Logging Configuration

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(app):
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set logging level based on environment
    if app.config.get('DEBUG'):
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    # File handler for general logs
    file_handler = RotatingFileHandler(
        'logs/alawael.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # File handler for error logs
    error_handler = RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    # File handler for security logs
    security_handler = RotatingFileHandler(
        'logs/security.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    security_handler.setLevel(logging.WARNING)
    security_formatter = logging.Formatter(
        '[%(asctime)s] SECURITY - %(levelname)s: %(message)s'
    )
    security_handler.setFormatter(security_formatter)
    
    # Console handler for development
    if app.config.get('DEBUG'):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        app.logger.addHandler(console_handler)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_handler)
    app.logger.setLevel(log_level)
    
    # Create security logger
    security_logger = logging.getLogger('security')
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.WARNING)
    
    app.logger.info('Application logging initialized')
    
    return app.logger, security_logger


def log_security_event(event_type, message, user_id=None, ip_address=None):
    """Log security-related events"""
    security_logger = logging.getLogger('security')
    
    log_message = f"{event_type}"
    if user_id:
        log_message += f" | User: {user_id}"
    if ip_address:
        log_message += f" | IP: {ip_address}"
    log_message += f" | {message}"
    
    security_logger.warning(log_message)


def log_user_action(action, user_id, details=""):
    """Log user actions for audit trail"""
    app_logger = logging.getLogger('flask.app')
    app_logger.info(f"User Action | User: {user_id} | Action: {action} | Details: {details}")

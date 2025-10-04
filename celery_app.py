"""
نقطة دخول تطبيق Celery
Celery Application Entry Point
"""
from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Celery
celery_app = Celery(
    'alawael_erp',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/2'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/3'),
    include=[
        'app.tasks.backup_tasks',
        'app.tasks.notification_tasks',
        'app.tasks.report_tasks',
        'app.tasks.ai_tasks',
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Riyadh',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3000,  # 50 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    # النسخ الاحتياطي اليومي
    'daily-database-backup': {
        'task': 'app.tasks.backup_tasks.backup_database',
        'schedule': crontab(hour=2, minute=0),  # 2:00 AM daily
    },
    
    # تنظيف الملفات المؤقتة
    'cleanup-temp-files': {
        'task': 'app.tasks.backup_tasks.cleanup_temp_files',
        'schedule': crontab(hour=3, minute=0),  # 3:00 AM daily
    },
    
    # إرسال التقارير الأسبوعية
    'weekly-progress-reports': {
        'task': 'app.tasks.report_tasks.send_weekly_reports',
        'schedule': crontab(day_of_week=6, hour=9, minute=0),  # Saturday 9:00 AM
    },
    
    # التذكير بالمواعيد
    'send-appointment-reminders': {
        'task': 'app.tasks.notification_tasks.send_appointment_reminders',
        'schedule': crontab(hour='8-18', minute=0),  # Every hour from 8 AM to 6 PM
    },
    
    # تحديث التحليلات الذكية
    'update-ai-analytics': {
        'task': 'app.tasks.ai_tasks.update_ai_analytics',
        'schedule': crontab(hour=1, minute=0),  # 1:00 AM daily
    },
    
    # فحص صحة النظام
    'system-health-check': {
        'task': 'app.tasks.monitoring_tasks.system_health_check',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}

if __name__ == '__main__':
    celery_app.start()

import os
from celery import Celery

# تنظیم متغیر محیطی برای تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# خواندن تنظیمات از فایل settings.py با پیشوند CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# جستجوی خودکار تسک‌ها در تمام اپلیکیشن‌های ثبت‌شده
app.autodiscover_tasks()
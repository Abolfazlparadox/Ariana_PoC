from celery import shared_task
from django.core.cache import cache
import time


@shared_task(bind=True)
def generate_heavy_financial_report(self, report_id):
    """
    این یک تسک سنگین شبیه‌سازی شده است که تولید آن زمان‌بر است.
    پس از اتمام، نتیجه را در ردیس کش می‌کند.
    """
    print(f"--- [Celery] شروع پردازش سنگین برای گزارش شماره {report_id} ---")

    # شبیه‌سازی پردازش سنگین (مثلاً کوئری‌های پیچیده یا جنریت کردن فایل PDF)
    time.sleep(10)

    report_data = {
        "report_id": report_id,
        "status": "Completed",
        "generated_by": "Celery Asynchronous Worker",
        "data": {
            "total_sales": 154000000,
            "total_profit": 42000000,
            "currency": "IRT"
        }
    }

    # ذخیره نتیجه در کش Redis به مدت ۱ ساعت (3600 ثانیه)
    cache.set(f"financial_report_{report_id}", report_data, timeout=3600)

    print(f"--- [Celery] گزارش {report_id} با موفقیت ساخته و کش شد! ---")
    return f"Report {report_id} Ready"
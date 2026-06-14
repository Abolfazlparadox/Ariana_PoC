from django.http import JsonResponse
from django.core.cache import cache
from .tasks import generate_heavy_financial_report


def get_report_view(request):
    # گرفتن ایدی گزارش از کوئری‌استرینگ (پیش‌فرض ۱)
    report_id = request.GET.get('id', 1)
    cache_key = f"financial_report_{report_id}"

    # ۱. بررسی حافظه کش Redis
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse({
            "source": "Redis Cache Engine (In-Memory)",
            "message": "دیتا مستقیماً از رم خوانده شد و پرفورمنس ۱۰۰٪ است.",
            "data": cached_data
        }, status=200, json_dumps_params={'ensure_ascii': False})

    # ۲. ارسال به صف Celery (در صورتی که در کش نبود)
    # با متد delay تسک رو بدون بلاک کردن سرور می‌فرستیم به ردیس
    task = generate_heavy_financial_report.delay(report_id)

    return JsonResponse({
        "source": "Celery Queue Management",
        "message": "گزارش در کش نبود. تسک سنگین به صف Celery ارسال شد و سرور بلاک نگردید.",
        "task_id": task.id,
        "hint": "لطفاً ۱۰ ثانیه دیگر همین دکمه/ریکوئست را مجدداً ارسال کنید تا دیتا را از کش بگیرید."
    }, status=202, json_dumps_params={'ensure_ascii': False})
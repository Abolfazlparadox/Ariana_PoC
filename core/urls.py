from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # کلمه .ext از اینجا حذف شد
    path('reports/', include('reports.urls')),
]
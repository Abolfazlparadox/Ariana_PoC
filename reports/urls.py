from django.urls import path
from .views import get_report_view

urlpatterns = [
    path('financial/', get_report_view, name='financial_report'),
]
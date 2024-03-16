from django.urls import path
from . import views
from .converters import FloatConverter


urlpatterns = [
    path('fee/', views.fee_detail, name='fee_detail'),
    path('fee_detail/', views.fee_detail, name='fee_detail'),
    path('fee_submission/<int:student_id>/', views.fee_submission, name='fee_submission'),
    path('fee_history/<int:student_id>/', views.fee_history, name='fee_history'),
    path('generate_receipt/<int:fee_id>/', views.generate_receipt, name='generate_receipt'),
    path('send_message/<int:student_id>/<float:remaining_amount>/', views.send_message, name='send_message'),
    path('fee_dashboard/', views.fee_dashboard, name='fee_dashboard'),
    path('fee_dashboard/api/', views.fee_dashboard_api, name='fee_dashboard_api'),
]


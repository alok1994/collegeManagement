from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboardpage'),
    path('api/user-count/', views.get_user_count, name='user_count_api'),
]

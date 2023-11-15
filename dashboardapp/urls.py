from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboardpage'),
    path('api/user-count/', views.get_user_count, name='user_count_api'),
    path('api/semester-wise-student-data/', views.get_semester_wise_student_data, name='semester_wise_student_data'),
]

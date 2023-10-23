from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('student-list/', views.student_list, name='student_list'),
    path('student-details/<int:student_id>/', views.student_details, name='student_details'),
    path('update_student/<int:student_id>/', views.update_student, name='update_student'),
    path('first_year/', views.first_year, name='first_year'),
    path('second_year/', views.second_year, name='second_year'),
    path('third_year/', views.third_year, name='third_year'),
    path('first_year/update/<int:student_id>/', views.update_student_first_year, name='update_student_first_year'),
    path('second_year/update/<int:student_id>/', views.update_student_second_year, name='update_student_second_year'),
    path('third_year/update/<int:student_id>/', views.update_student_third_year, name='update_student_third_year'),
    path('student-list/delete/<int:student_id>/', views.delete_student, name='delete_student'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

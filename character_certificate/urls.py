from django.urls import path
from . import views

urlpatterns = [
    path('student_detail_char_cert/', views.student_list_details, name='student_list_details'),
    #path('generate/<int:student_id>/', views.generate_character_certificate, name='generate_character_certificate'),
    path('view/<int:student_id>/', views.view_character_certificate, name='view_character_certificate'),
]

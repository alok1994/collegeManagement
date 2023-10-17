from django.urls import path
from . import views

urlpatterns = [
    path('student_detail_trans_cert/', views.student_list_details_trans, name='student_list_details_transfer'),
    #path('generate/<int:student_id>/', views.generate_character_certificate, name='generate_character_certificate'),
    path('view_tc/<int:student_id>/', views.view_transfer_certificate, name='view_transfer_certificate'),
]

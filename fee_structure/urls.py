from django.urls import path
from . import views

urlpatterns = [
    path('fee-structure/', views.fee_structure, name='fee_structure'),
    path('update-semester-fee/<int:semester_number>/', views.update_semester_fee, name='update_semester_fee'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('admission/', views.admission_form, name='admission_form'),
    path('admission/success/', views.admission_success, name='admission_success'),
]

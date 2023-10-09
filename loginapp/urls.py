from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    #path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.logout_view, name='logout'),
]

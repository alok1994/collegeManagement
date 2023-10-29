# messagingapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_messages, name='send_messages'),
    path('message-sent/', views.message_sent, name='message_sent')

]

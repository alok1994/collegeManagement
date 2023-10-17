from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admission/', views.admission_form, name='admission_form'),
    path('admission/success/', views.admission_success, name='admission_success'),
    path('student-data-api/', views.student_data_api, name='student_data_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
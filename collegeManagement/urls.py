from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('loginapp.urls')),
    path('dashboard/', include('dashboardapp.urls')),
    path('admission/', include('admissionapp.urls')),
    path('student-list/', include('student_list.urls')),
    path('fee_management/', include('fee_management.urls')),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

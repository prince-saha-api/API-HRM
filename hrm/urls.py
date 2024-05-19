from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('auth/', include('user_auth.urls')),
    path('api/user/', include('user.urls')),
    path('api/contribution/', include('contribution.urls')),
    path('api/facility/', include('facility.urls')),
    path('api/company/', include('company.urls')),
    path('api/branch/', include('branch.urls')),
    path('api/department/', include('department.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/workingshift/', include('workingshift.urls')),
    path('api/officialoffday/', include('officialoffday.urls')),
    path('api/salarycalculation/', include('salarycalculation.urls')),
    path('api/costcalculation/', include('costcalculation.urls')),
    path('api/hrm_settings/', include('hrm_settings.urls')),
    path('api/bonusmanagement/', include('bonusmanagement.urls')),
    path('api/device/', include('device.urls')),
    path('api/leave/', include('leave.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
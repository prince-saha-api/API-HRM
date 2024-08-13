from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include



from user import models as MODELS_USER
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
@api_view(['GET'])
def createUser(request, username=None, password=None):
    try:
        if username and password:
            MODELS_USER.User.objects.create_user(username=username, password=password)
            return Response({'message': 'User created!', 'username': username, 'password': password}, status=status.HTTP_201_CREATED)
        else:
            MODELS_USER.User.objects.create_user(username='admin', password='admin')
            return Response({'message': 'User created!', 'username': 'admin', 'password': 'admin'}, status=status.HTTP_201_CREATED)
    except: return Response({'message': 'Couldn\'t create user!', 'username': '', 'password': ''}, status=status.HTTP_400_BAD_REQUEST)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('__admin__/<str:username>/<str:password>', createUser, name='__admin__'),
    
    path('auth/', include('user_auth.urls')),
    path('api/user/', include('user.urls')),
    path('api/contribution/', include('contribution.urls')),
    path('api/facility/', include('facility.urls')),
    path('api/company/', include('company.urls')),
    path('api/branch/', include('branch.urls')),
    path('api/department/', include('department.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/hrm_settings/', include('hrm_settings.urls')),
    path('api/device/', include('device.urls')),
    path('api/leave/', include('leave.urls')),
    path('api/payroll/', include('payroll.urls')),
    path('api/jobrecord/', include('jobrecord.urls')),
    path('api/notice/', include('notice.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
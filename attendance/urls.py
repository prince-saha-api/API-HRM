from django.urls import path
from attendance import views

urlpatterns = [
    path('manual-attendence/', views.manualattendence, name='manual-attendence'),
    path('attendance-from-logs-all-devices/<int:minutes>', views.attendancefromlogsalldevices, name='attendance-from-logs-all-devices'),
    path('remote-attendance/<int:userid>/<str:date>', views.remoteattendance, name='remote-attendance'),
]

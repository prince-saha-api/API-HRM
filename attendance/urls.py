from django.urls import path
from attendance import views

urlpatterns = [
    path('add-manual-attendence/', views.addmanualattendence, name='add-manual-attendence'),
    path('add-attendance-from-logs-all-devices/<int:minutes>', views.addattendancefromlogsalldevices, name='add-attendance-from-logs-all-devices'),
    path('add-remote-attendance/<int:userid>/<str:date>', views.addremoteattendance, name='add-remote-attendance'),
]

from django.urls import path
from attendance import views

urlpatterns = [
    path('get-manual-attendence/', views.getmanualattendence, name='get-manual-attendence'),
    path('add-manual-attendence/', views.addmanualattendence, name='add-manual-attendence'),
    path('get-loggedin-users-manual-attendence/', views.getloggedinusersmanualattendence, name='get-loggedin-users-manual-attendence'),
    path('update-manual-attendence/<int:manualattendenceid>', views.updatemanualattendence, name='update-manual-attendence'),

    path('add-attendance-from-logs-all-devices/<int:minutes>', views.addattendancefromlogsalldevices, name='add-attendance-from-logs-all-devices'),
    path('add-remote-attendance/<int:userid>/<str:date>', views.addremoteattendance, name='add-remote-attendance'),
]

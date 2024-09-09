from django.urls import path
from attendance import views

urlpatterns = [
    path('calculate-attendance/', views.calculateattendance, name='calculate-attendance'),


    path('get-manual-attendence/', views.getmanualattendence, name='get-manual-attendence'),
    path('add-manual-attendence/', views.addmanualattendence, name='add-manual-attendence'),
    path('update-manual-attendence/<int:manualattendenceid>', views.updatemanualattendence, name='update-manual-attendence'),
    path('approve-manual-attendence/<int:manualattendenceid>', views.approvemanualattendence, name='approve-manual-attendence'),
    path('reject-manual-attendence/<int:manualattendenceid>', views.rejectmanualattendence, name='reject-manual-attendence'),

    path('get-remote-log/', views.getremotelog, name='get-remote-log'),
    path('add-remote-log/', views.addremotelog, name='add-remote-log'),
    path('update-remote-log/<int:remotelogid>', views.updateremotelog, name='update-remote-log'),
    path('delete-remote-log/<int:remotelogid>', views.deleteremotelog, name='delete-remote-log'),

    path('get-remote-attendance/', views.getremoteattendance, name='get-remote-attendance'),
    path('add-remote-attendance/', views.addremoteattendance, name='add-remote-attendance'),
    path('delete-remote-attendance/<int:deleteattendenceid>', views.deleteremoteattendance, name='delete-remote-attendance'),
    path('get-loggedin-users-remote-attendence/', views.getloggedinusersremoteattendence, name='get-loggedin-users-remote-attendence'),
    # path('update-remote-attendence/<int:remoteattendenceid>', views.updateremoteattendence, name='update-remote-attendence'),
    path('approve-remote-attendence/<int:remoteattendenceid>', views.approveremoteattendence, name='approve-remote-attendence'),
    path('reject-remote-attendence/<int:remoteattendenceid>', views.rejectremoteattendence, name='reject-remote-attendence'),

    path('attendance-from-logs/<int:minutes>', views.attendancefromlogs, name='attendance-from-logs'),
]

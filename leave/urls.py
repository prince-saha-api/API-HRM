from django.urls import path
from leave import views

urlpatterns = [
    path('get-leavepolicy/', views.getleavepolicys, name='get-leavepolicy'),
    path('add-leavepolicy/', views.addleavepolicy, name='add-leavepolicy'),
    path('update-leavepolicy/<int:leavepolicyid>', views.updateleavepolicy, name='update-leavepolicy'),

    path('assign-leavepolicy/', views.assignleavepolicy, name='assign-leave-policy'),
    path('get-assign-leavepolicy/', views.getassignleavepolicys, name='get-assign-leave-policy'),
    
    path('get-leavesummary/', views.getleavesummarys, name='get-leavesummary'),
    
    path('get-leaverequest/', views.getleaverequest, name='get-leaverequest'),
    path('add-leaverequest/', views.addleaverequest, name='add-leaverequest'),
    path('approve-leaverequest/<int:leaverequest>', views.approveleaverequest, name='approve-leaverequest'),

    path('get-leaveallocationrequest/', views.getleaveallocationrequest, name='get-leaveallocationrequest'),
    path('add-leaveallocationrequest/', views.addleaveallocationrequest, name='add-leaveallocationrequest'),
    path('approve-leaveallocationrequest/<int:leaveallocationrequest>', views.approverequestleaveallocation, name='approve-leaveallocationrequest'),

    path('get-holiday/', views.getholidays, name='get-holiday'),
    path('add-holiday/', views.addholiday, name='add-holiday'),
    path('update-holiday/<int:holidayid>', views.updateholiday, name='update-holiday'),
]

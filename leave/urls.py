from django.urls import path
from leave import views

urlpatterns = [
    path('get-leavepolicy/', views.getleavepolicys, name='get-leavepolicy'),
    path('add-leavepolicy/', views.addleavepolicy, name='add-leavepolicy'),
    path('update-leavepolicy/<int:leavepolicyid>', views.updateleavepolicy, name='update-leavepolicy'),
    path('delete-leavepolicy/<int:leavepolicyid>', views.deleteleavepolicy, name='delete-leavepolicy'),

    path('get-assign-leavepolicy/', views.getassignleavepolicys, name='get-assign-leave-policy'),
    path('assign-leavepolicy/', views.assignleavepolicy, name='assign-leave-policy'),
    path('remove-assigned-leavepolicy/<int:leavepolicyassignid>', views.removeassignedleavepolicy, name='remove-assigned-leavepolicy'),
    
    path('get-leavesummary/', views.getleavesummarys, name='get-leavesummary'),
    
    path('get-leaverequest/', views.getleaverequest, name='get-leaverequest'),
    path('add-leaverequest/', views.addleaverequest, name='add-leaverequest'),
    path('approve-leaverequest/<int:leaverequestid>', views.approveleaverequest, name='approve-leaverequest'),
    path('reject-leaverequest/<int:leaverequestid>', views.rejectleaverequest, name='reject-leaverequest'),

    # path('get-leaveallocationrequest/', views.getleaveallocationrequest, name='get-leaveallocationrequest'),
    path('add-leaveallocationrequest/', views.addleaveallocationrequest, name='add-leaveallocationrequest'),
    path('approve-leaveallocationrequest/<int:leaveallocationrequestid>', views.approverequestleaveallocation, name='approve-leaveallocationrequest'),

    path('get-holiday/', views.getholidays, name='get-holiday'),
    path('add-holiday/', views.addholiday, name='add-holiday'),
    path('update-holiday/<int:holidayid>', views.updateholiday, name='update-holiday'),
    path('delete-holiday/<int:holidayid>', views.deleteholiday, name='delete-holiday'),
]

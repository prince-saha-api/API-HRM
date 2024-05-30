from django.urls import path
from leave import views

urlpatterns = [
    path('get-leavepolicy/', views.getleavepolicys, name='get-leavepolicy'),
    path('add-leavepolicy/', views.addleavepolicy, name='add-leavepolicy'),
    path('assign-leavepolicy/', views.assignleavepolicy, name='assign-leave-policy'),

    path('get-leavesummary/', views.getleavesummarys, name='get-leavesummary'),
    
    path('get-leaverequest/', views.getleaverequest, name='get-leaverequest'),
    path('add-leaverequest/', views.addleaverequest, name='add-leaverequest'),
    path('approve-leaverequest/<int:leaverequest>', views.approveleaverequest, name='approve-leaverequest'),

    path('get-leaveallocationrequest/', views.getleaveallocationrequest, name='get-leaveallocationrequest'),
    path('add-leaveallocationrequest/', views.addleaveallocationrequest, name='add-leaveallocationrequest'),
    path('approve-leaveallocationrequest/<int:leaveallocationrequest>', views.approverequestleaveallocation, name='approve-leaveallocationrequest')
]

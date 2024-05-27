from django.urls import path
from leave import views

urlpatterns = [
    path('get-leavepolicy/', views.getleavepolicys, name='get-leavepolicy'),
    path('add-leavepolicy/', views.addleavepolicy, name='add-leavepolicy'),

    path('get-leavesummary/', views.getleavesummarys, name='get-leavesummary'),
    path('get-users-leave-summarys/<int:userid>', views.getusersleavesummarys, name='get-users-leave-summarys'),

    path('assign-leavepolicy/', views.assignleavepolicy, name='assign-leave-policy'),
    path('get-users-assigned-leavepolicy/<int:userid>', views.getusersassignedleavepolicy, name='get-users-assigned-leavepolicy'),
    path('get-users-unassigned-leavepolicy/<int:userid>', views.getusersunassignedleavepolicy, name='get-users-unassigned-leavepolicy'),

    path('add-leaverequest/', views.addleaverequest, name='add-leaverequest'),
    path('approve-leaverequest/<int:leaverequest>', views.approveleaverequest, name='approve-leaverequest'),
    path('get-filtered-leaverequest/', views.getfilteredleaverequest, name='get-filtered-leaverequest'),

    path('leave-allocation-request/', views.requestleaveallocation, name='leave-allocation-request'),
    path('approve-leave-allocation-request/<int:leaveallocationrequest>', views.approverequestleaveallocation, name='approve-leave-allocation-request'),
]

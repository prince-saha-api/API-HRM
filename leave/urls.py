from django.urls import path
from leave import views

urlpatterns = [
    path('assign-leave-policy/', views.assignleavepolicy, name='assign-leave-policy'),
    path('leave-request/', views.leaverequest, name='leave-request'),
    path('approve-leave-request/<int:leaverequest>', views.approveleaverequest, name='approve-leave-request'),
    path('get-leavepolicy/', views.getleavepolicys, name='get-leavepolicy'),
    path('add-leavepolicy/', views.addleavepolicy, name='add-leavepolicy'),
]

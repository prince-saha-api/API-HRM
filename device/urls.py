from django.urls import path
from device import views

urlpatterns = [
    path('get-device/', views.getdevices, name='get-device'),
    path('add-device/', views.adddevice, name='add-device'),
    path('update-device/<int:deviceid>', views.updatedevice, name='update-device'),
    path('delete-device/<int:deviceid>', views.deletedevice, name='delete-device'),
    
    path('get-group/', views.getgroups, name='get-group'),
    path('add-group/', views.addgroup, name='add-group'),
    path('update-group/<int:groupid>', views.updategroup, name='update-group'),
    path('delete-group/<int:groupid>', views.deletegroup, name='delete-group'),

    path('get-devicegroup/', views.getdevicegroup, name='get-devicegroup'),
    path('add-devicegroup/', views.adddevicegroup, name='add-devicegroup'),
]

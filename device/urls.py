from django.urls import path
from device import views

urlpatterns = [
    path('get-device/', views.getdevices, name='get-device'),
    path('add-device/', views.adddevice, name='add-device'),
    path('update-device/<int:deviceid>', views.updatedevice, name='update-device'),
    
    path('get-devicegroup/', views.getdevicegroups, name='get-devicegroup'),
    path('add-devicegroup/', views.adddevicegroup, name='add-devicegroup'),
    path('update-devicegroup/<int:devicegroupid>', views.updatedevicegroup, name='update-devicegroup'),
]

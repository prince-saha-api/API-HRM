from django.urls import path
from facility import views

urlpatterns = [
    path('get-facility/', views.getfacilitys, name='get-facility'),
    path('add-facility/', views.addfacility, name='add-facility'),
    path('update-facility/<int:facilityid>', views.updatefacility, name='update-facility'),
]

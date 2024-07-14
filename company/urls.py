from django.urls import path
from company import views

urlpatterns = [
    path('get-company/', views.getcompanys, name='get-company'),
    path('add-company/', views.addcompany, name='add-company'),
    path('update-company/<int:companyid>', views.updatecompany, name='update-company'),
    
    path('get-basicinformation/', views.getbasicinformations, name='get-basicinformation'),
    path('add-basicinformation/', views.addbasicinformation, name='add-basicinformation'),
    path('update-basicinformation/<int:basicinformationid>', views.updatebasicinformation, name='update-basicinformation')
]
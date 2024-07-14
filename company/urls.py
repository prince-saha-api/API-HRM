from django.urls import path
from company import views

urlpatterns = [
    path('get-company/', views.getcompanys, name='get-company'),
    path('add-company/', views.addcompany, name='add-company'),
    path('delete-company/<int:companyid>', views.deletecompany, name='delete-company'),
    
    path('get-basicinformation/', views.getbasicinformations, name='get-basicinformation'),
    path('update-basicinformation/<int:basicinformationid>', views.updatebasicinformation, name='update-basicinformation'),
    path('delete-basicinformation/<int:basicinformationid>', views.deletebasicinformation, name='delete-basicinformation')
]
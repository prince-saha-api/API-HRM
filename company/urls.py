from django.urls import path
from company import views

urlpatterns = [
    path('get-company/', views.getcompanys, name='get-company'),
    path('add-company/', views.addcompany, name='add-company'),
    path('update-company/<int:companyid>', views.updatecompany, name='update-company'),
    
    path('get-basicinformation/', views.getbasicinformations, name='get-basicinformation'),
    path('add-basicinformation/', views.addbasicinformation, name='add-basicinformation'),
    path('update-basicinformation/<int:basicinformationid>', views.updatebasicinformation, name='update-basicinformation'),
    
    path('get-companytype/', views.getcompanytypes, name='get-companytype'),
    path('add-companytype/', views.addcompanytype, name='add-companytype'),
    path('update-companytype/<int:companytypeid>', views.updatecompanytype, name='update-companytype'),
    path('delete-companytype/<int:companytypeid>', views.deletecompanytype, name='delete-companytype')
]
from django.urls import path
from company import views

urlpatterns = [
    path('get-company/', views.getcompanys, name='get-company'),
    path('add-company/', views.addcompany, name='add-company'),
    path('get-basicinformation/', views.getbasicinformations, name='get-basicinformation'),
    path('add-basicinformation/', views.addbasicinformation, name='add-basicinformation'),
    path('get-companytype/', views.getcompanytypes, name='get-companytype'),
    path('add-companytype/', views.addcompanytype, name='add-companytype'),
]
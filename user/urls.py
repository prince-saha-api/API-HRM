from django.urls import path
from user import views
urlpatterns = [
    path('get-responsibility/', views.getresponsibilitys, name='get-responsibility'),
    path('add-responsibility/', views.addresponsibility, name='add-responsibility'),
    path('get-requiredskill/', views.getrequiredskills, name='get-requiredskill'),
    path('add-requiredskill/', views.addrequiredskill, name='add-requiredskill'),
    path('get-dsignation/', views.getdsignations, name='get-dsignation'),
    path('add-dsignation/', views.adddsignation, name='add-dsignation'),
    path('get-grade/', views.getgrades, name='get-grade'),
    path('add-grade/', views.addgrade, name='add-grade'),
    path('get-shift/', views.getshifts, name='get-shift'),
    path('add-shift/', views.addshift, name='add-shift'),
    path('get-employee/', views.getemployee, name='get-employee'),
    path('add-employee/', views.addemployee, name='add-employee'),
]

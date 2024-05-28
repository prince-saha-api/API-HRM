from django.urls import path
from company import views

urlpatterns = [
    path('get-company/', views.getcompanys, name='get-company'),
    path('add-company/', views.addcompany, name='add-company')
]
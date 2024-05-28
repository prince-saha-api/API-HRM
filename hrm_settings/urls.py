from django.urls import path
from hrm_settings import views

urlpatterns = [
    path('get-fiscalyear/', views.getfiscalyears, name='get-fiscalyear'),
    path('add-fiscalyear/', views.addfiscalyear, name='add-fiscalyear'),
]

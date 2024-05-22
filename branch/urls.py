from django.urls import path
from branch import views

urlpatterns = [
    path('get-branch/', views.getbranchs, name='get-branch'),
    path('add-branch/', views.addbranch, name='add-branch'),
    path('get-operatinghour/', views.getoperatinghours, name='get-operatinghour'),
    path('add-operatinghour/', views.addoperatinghour, name='add-operatinghour'),
]
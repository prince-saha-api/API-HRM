from django.urls import path
from contribution import views

urlpatterns = [
    path('get-address/', views.getaddresss, name='get-address'),
    path('add-address/', views.addaddress, name='add-address'),
    path('get-bankaccounttype/', views.getbankaccounttypes, name='get-bankaccounttype'),
    path('add-bankaccounttype/', views.addbankaccounttype, name='add-bankaccounttype'),
    path('get-bankaccount/', views.getbankaccounts, name='get-bankaccount'),
    path('add-bankaccount/', views.addbankaccount, name='add-bankaccount'),
]

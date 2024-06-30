from django.urls import path
from contribution import views

urlpatterns = [
    path('get-address/', views.getaddresss, name='get-address'),
    path('add-address/', views.addaddress, name='add-address'),
    path('update-address/<int:addressid>', views.updateaddress, name='update-address'),
    path('delete-address/<int:addressid>', views.deleteaddress, name='delete-address'),

    path('get-bankaccounttype/', views.getbankaccounttypes, name='get-bankaccounttype'),
    path('add-bankaccounttype/', views.addbankaccounttype, name='add-bankaccounttype'),
    path('update-bankaccounttype/<int:bankaccounttypeid>', views.updatebankaccounttype, name='update-bankaccounttype'),
    path('delete-bankaccounttype/<int:bankaccounttypeid>', views.deletebankaccounttype, name='delete-bankaccounttype'),

    path('get-bankaccount/', views.getbankaccounts, name='get-bankaccount'),
    path('add-bankaccount/', views.addbankaccount, name='add-bankaccount'),
]

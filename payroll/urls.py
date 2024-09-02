from django.urls import path
from payroll import views

urlpatterns = [
    path('get-payrollearning/', views.getpayrollearnings, name='get-payrollearning'),
    path('add-payrollearning/', views.addpayrollearning, name='add-payrollearning'),
    path('update-payrollearning/<int:payrollearningid>', views.updatepayrollearning, name='update-payrollearning'),
    path('delete-payrollearning/<int:payrollearningid>', views.deletepayrollearning, name='delete-payrollearning'),

    path('get-payrolldeduction/', views.getpayrolldeductions, name='get-payrolldeduction'),
    path('add-payrolldeduction/', views.addpayrolldeduction, name='add-payrolldeduction'),
    path('update-payrolldeduction/<int:payrolldeductionid>', views.updatepayrolldeduction, name='update-payrolldeduction'),
    path('delete-payrolldeduction/<int:payrolldeductionid>', views.deletepayrolldeduction, name='delete-payrolldeduction'),

    path('get-payrolltax/', views.getpayrolltaxs, name='get-payrolltax'),
    path('add-payrolltax/', views.addpayrolltax, name='add-payrolltax'),
    path('update-payrolltax/<int:payrolltaxid>', views.updatepayrolltax, name='update-payrolltax'),
    path('delete-payrolltax/<int:payrolltaxid>', views.deletepayrolltax, name='delete-payrolltax'),
]

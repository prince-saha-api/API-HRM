from django.urls import path
from notice import views

urlpatterns = [
    path('add-noticeboard/', views.addnoticeboard, name='add-noticeboard'),

    path('get-noticeboard/', views.getnoticeboards, name='get-noticeboard'),
    path('get-noticeboardcompany/', views.getnoticeboardcompanys, name='get-noticeboardcompany'),
    path('get-noticeboardbranch/', views.getnoticeboardbranch, name='get-noticeboardbranch'),
    path('get-noticeboarddepartment/', views.getnoticeboarddepartment, name='get-noticeboarddepartment'),
    path('get-noticeboardemployee/', views.getnoticeboardemployee, name='get-noticeboardemployee'),

    path('update-noticeboard/<int:noticeid>', views.updatenoticeboard, name='update-noticeboard'),
    path('delete-noticeboard/<int:noticeid>', views.deletenoticeboard, name='delete-noticeboard'),

    # path('get-payrolldeduction/', views.getpayrolldeductions, name='get-payrolldeduction'),
    # path('add-payrolldeduction/', views.addpayrolldeduction, name='add-payrolldeduction'),
    # path('update-payrolldeduction/<int:payrolldeductionid>', views.updatepayrolldeduction, name='update-payrolldeduction'),

    # path('get-payrolltax/', views.getpayrolltaxs, name='get-payrolltax'),
    # path('add-payrolltax/', views.addpayrolltax, name='add-payrolltax'),
    # path('update-payrolltax/<int:payrolltaxid>', views.updatepayrolltax, name='update-payrolltax'),
]

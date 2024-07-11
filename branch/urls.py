from django.urls import path
from branch import views

urlpatterns = [
    path('get-operatinghour/', views.getoperatinghours, name='get-operatinghour'),
    path('add-operatinghour/', views.addoperatinghour, name='add-operatinghour'),
    path('update-operatinghour/<int:operatinghourid>', views.updateoperatinghour, name='update-operatinghour'),
    path('delete-operatinghour/<int:operatinghourid>', views.deleteoperatinghour, name='delete-operatinghour'),

    path('get-branch/', views.getbranchs, name='get-branch'),
    path('add-branch/', views.addbranch, name='add-branch'),
    path('update-branch/<int:branchid>', views.updatebranch, name='update-branch'),
    path('delete-branch/<int:branchid>', views.deletebranch, name='delete-branch')
]
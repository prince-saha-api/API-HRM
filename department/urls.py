from django.urls import path
from department import views

urlpatterns = [
    path('get-department/', views.getdepartments, name='get-department'),
    path('add-department/', views.adddepartment, name='add-department'),
    path('update-department/<int:departmentid>', views.updatedepartment, name='update-department'),
    path('delete-department/<int:departmentid>', views.deletedepartment, name='delete-department'),
]

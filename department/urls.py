from django.urls import path
from department import views

urlpatterns = [
    path('get-department/', views.getdepartments, name='get-department'),
    # path('add-department/', views.addemployee, name='add-department'),
]

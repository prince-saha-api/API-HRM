from django.urls import path
from user import views
urlpatterns = [
    path('get-employee/', views.getemployee, name='get-employee'),
]

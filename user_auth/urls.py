from django.urls import path, include
from user_auth import views
from user_auth.paramstotoken import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', views.LogoutAllView.as_view(), name='auth_logout_all'),
    
    path('reset-password/', views.resetPassword, name='reset-password'),
]
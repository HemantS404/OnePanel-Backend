from django.urls import path
from .views import RegistrationAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('register/', RegistrationAPI.as_view(), name = 'register_user'),
    path('logout/',  TokenBlacklistView.as_view(), name = 'logout_user'),
    path('login/', TokenObtainPairView.as_view(), name = 'login_user'),
    path('token-refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]
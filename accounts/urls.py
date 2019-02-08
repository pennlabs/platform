from django.urls import path
from accounts.views import LoginView, PlatformTokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("verify/", PlatformTokenVerifyView.as_view()),
]

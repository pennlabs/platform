from django.urls import path
from accounts.views import LoginView
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("refresh/", refresh_jwt_token),
    path("verify/", verify_jwt_token),
]

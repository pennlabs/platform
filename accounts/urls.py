from django.urls import path
from accounts.views import LoginView
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("verify/", verify_jwt_token),
]

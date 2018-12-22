from django.urls import path, include
from accounts.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
]

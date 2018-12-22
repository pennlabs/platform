from django.urls import path, include
# from knox.views import LogoutView, LogoutAllView
from accounts.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    # path("logout/", LogoutView.as_view()),
    # path("logoutall/", LogoutAllView.as_view()),
]

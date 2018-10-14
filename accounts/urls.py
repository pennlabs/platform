from .views import RegistrationView, LoginView, UserView
from knox.views import LogoutView, LogoutAllView
from django.urls import path, include

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("logoutall/", LogoutAllView.as_view()),
    path("users/", UserView.as_view({'get': 'list'}))
]

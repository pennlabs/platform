from .views import RegistrationView, LoginView, UserView
from django.urls import path, include

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path("users/", UserView.as_view({'get': 'list'}))
]

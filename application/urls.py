from django.urls import path
from application.views import splash

urlpatterns = [
    path("", splash)
]

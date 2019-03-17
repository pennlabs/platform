from django.urls import path
from application.views import splash


app_name = 'application'


urlpatterns = [
    path("", splash, name='homepage')
]

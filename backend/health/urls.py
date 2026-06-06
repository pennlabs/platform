from django.urls import path
from health.views import HealthView


app_name = "health"

urlpatterns = [
    path("", HealthView.as_view(), name="health"),
]

from django.urls import path
from health.views import HealthView


app_name = "health"

urlpatterns = [
    path("backend/", HealthView.as_view(), name="backend"),
]

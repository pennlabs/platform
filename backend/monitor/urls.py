from django.urls import path
from monitor.views import PullsView


app_name = "monitor"


urlpatterns = [
    path("pulls/", PullsView.as_view(), name="pulls"),
]

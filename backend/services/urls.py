from django.urls import path

from services.views import ServiceViewSet, UpdateViewSet


app_name = "services"


urlpatterns = [
    path("services/", ServiceViewSet.as_view({"get": "list"}), name="services"),
    path("updates/", UpdateViewSet.as_view({"get": "list"}), name="updates"),
]

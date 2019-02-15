from django.urls import path
from services.views import ServiceViewSet, UpdateViewSet

urlpatterns = [
    path("services/", ServiceViewSet.as_view({'get': 'list'})),
    path("updates/", UpdateViewSet.as_view({'get': 'list'})),
]

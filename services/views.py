from rest_framework import viewsets

from services.models import Service, Update
from services.serializers import ServiceSerializer, UpdateSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs services.
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    http_method_names = ["get"]


class UpdateViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs updates.
    """

    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    http_method_names = ["get"]

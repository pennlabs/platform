from rest_framework import viewsets
from .models import LabMember, Product, Update, Event
from .serializers import LabMemberSerializer, ProductSerializer, UpdateSerializer, EventSerializer


class LabMemberViewSet(viewsets.ModelViewSet):
    queryset = LabMember.objects.all()
    serializer_class = LabMemberSerializer
    http_method_names = ['get']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']


class UpdateViewSet(viewsets.ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    http_method_names = ['get']


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']

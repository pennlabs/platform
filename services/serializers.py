from rest_framework import serializers

from services.models import Service, Update


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("name", "description", "location", "icon", "team", "notes")


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ("service", "title", "body")

from rest_framework import serializers
from clubs.models import Club, Event


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('name', 'route', 'founded', 'verified', 'contact', 'description')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'club', 'time', 'location', 'url', 'description')
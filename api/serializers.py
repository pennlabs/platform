from rest_framework import serializers
from accounts.models import User
from .models import LabMember, Team, Update, Event


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'date_joined', 'name', 'major', 'school')


class LabMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = LabMember
        fields = ('user', 'bio', 'location', 'role', 'photo', 'linkedin', 'website', 'github', 'year_joined')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'tagline', 'description', 'url')


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ('product', 'title', 'body')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'date', 'location', 'start_time', 'end_time', 'link', 'free_food')

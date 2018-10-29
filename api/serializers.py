from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Member, Team, Role, Update, Event


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'tagline', 'description', 'url')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'description')


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    teams = TeamSerializer(read_only=True, many=True)
    roles = RoleSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = ('user', 'bio', 'location', 'teams', 'roles', 'photo', 'linkedin', 'website', 'github', 'year_joined', 'alumnus')


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ('product', 'title', 'body')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'date', 'location', 'start_time', 'end_time', 'link', 'free_food')

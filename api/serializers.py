from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from api.models import Member, Team, Role, Update


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
        fields = ('user', 'bio', 'location', 'teams', 'roles', 'url', 'photo', 'linkedin', 'website', 'github', 'year_joined', 'alumnus')


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ('product', 'title', 'body')
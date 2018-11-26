from rest_framework import serializers
from shortener.models import Url
from accounts.models import User
from accounts.serializers import UserSerializer
from org.models import Member, Team, Role


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('short_id',)


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
        fields = ('user', 'bio', 'location', 'teams', 'roles', 'url', 'photo', 'linkedin', 'website', 'github',
            'year_joined', 'alumnus')

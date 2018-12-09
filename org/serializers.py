from rest_framework import serializers
from shortener.models import Url
from accounts.models import User
from accounts.serializers import UserSerializer
from org.models import Member, Team, Role


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('short_id',)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'description')


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    team = serializers.StringRelatedField()
    roles = RoleSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = ('user', 'bio', 'location', 'team', 'roles', 'url', 'photo', 'linkedin', 'website', 'github',
            'year_joined', 'alumnus')


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(required=True, many=True)

    class Meta:
        model = Team
        fields = ('name', 'tagline', 'description', 'url', 'members')

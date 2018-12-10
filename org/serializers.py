from rest_framework import serializers
from shortener.models import Url
from accounts.serializers import StudentSerializer
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
    student = StudentSerializer(required=True)
    team = serializers.StringRelatedField()
    roles = RoleSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = ('student', 'bio', 'location', 'team', 'roles', 'url', 'photo', 'linkedin', 'website', 'github',
            'year_joined', 'alumnus')


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(required=True, many=True)

    class Meta:
        model = Team
        fields = ('name', 'tagline', 'description', 'url', 'members')

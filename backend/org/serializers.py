from django.db.models import Min
from rest_framework import serializers
from shortener.models import Url

from accounts.models import Student
from org.models import Member, Role, Team


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ("long_url", "short_id")
        read_only_fields = ("short_id",)

    def create(self, validated_data):
        url, _ = Url.objects.get_or_create(validated_data.get("long_url"))
        return url


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("name", "description")


class UserField(serializers.RelatedField):
    def to_representation(self, value):
        return value.get_full_name()


class StudentSerializer(serializers.ModelSerializer):
    name = UserField(source="user", read_only=True)

    class Meta:
        model = Student
        fields = ("name", "major", "school")


class MemberSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=True)
    team = serializers.StringRelatedField()
    roles = RoleSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = (
            "student",
            "bio",
            "location",
            "team",
            "roles",
            "url",
            "photo",
            "linkedin",
            "website",
            "github",
            "year_joined",
            "alumnus",
            "graduation_year",
            "job",
        )


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    def get_members(self, instance):
        members = (
            Member.objects.filter(team__id=instance.id, alumnus=False)
            .annotate(order=Min("roles__order"))
            .order_by("order")
        )
        return MemberSerializer(members, many=True).data

    class Meta:
        model = Team
        fields = ("name", "description", "members")

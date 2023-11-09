from announcements.models import Announcement, Audience
from rest_framework import serializers


class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ("name",)


class AnnouncementSerializer(serializers.ModelSerializer):
    audiences = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Audience.objects.all()
    )

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "message",
            "announcement_type",
            "release_time",
            "end_time",
            "audiences",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["audiences"] = [
            audience.name for audience in instance.audiences.all()
        ]
        return representation

    def to_internal_value(self, data):
        audiences = data.get("audiences")
        if isinstance(audiences, list):
            if not audiences:
                raise serializers.ValidationError(
                    {"detail": "You must provide at least one audience"}
                )
            audience_objs = []
            for audience_name in audiences:
                audience = Audience.objects.filter(name=audience_name).first()
                if not audience:
                    raise serializers.ValidationError(
                        {"detail": f"Invalid audience name: {audience_name}"}
                    )
                audience_objs.append(audience)
            data["audiences"] = audience_objs
        return super().to_internal_value(data)

    def create(self, validated_data):
        audiences = validated_data.pop("audiences")
        instance = Announcement.objects.create(**validated_data)
        instance.audiences.set(audiences)
        return instance

    def update(self, instance, validated_data):
        audiences = validated_data.pop("audiences", None)
        super().update(instance, validated_data)
        if audiences:
            instance.audiences.set(audiences)
        return instance

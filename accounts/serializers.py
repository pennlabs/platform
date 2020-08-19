from rest_framework import serializers

from accounts.models import Email, PhoneNumberModel, Student, User


class UserSerializer(serializers.ModelSerializer):
    # SerializerMethodFields are read_only
    first_name = serializers.CharField(source="get_preferred_name", required=False)
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    user_permissions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="codename"
    )
    product_permission = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="codename", source="user_permissions"
    )  # TODO: remove this once all products update to new version of DLA

    class Meta:
        model = User
        fields = (
            "pennid",
            "first_name",
            "last_name",
            "username",
            "email",
            "groups",
            "product_permission",
            "user_permissions",
        )

        read_only_fields = (
            "pennid",
            "last_name",
            "username",
            "email",
            "groups",
            "product_permission",
            "user_permissions",
        )

    def update(self, instance, validated_data):
        instance.preferred_name = validated_data.get("get_preferred_name", instance.preferred_name)
        if instance.preferred_name == instance.first_name:
            instance.preferred_name = ""

        instance.save()
        return instance


class UserSearchSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def get_first_name(self, obj):
        return obj.get_preferred_name()


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = ("user", "major", "school")

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop("user")
        for key in user_representation:
            if key != "pennid":
                representation[key] = user_representation[key]
        return representation


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumberModel
        fields = ["phone_number", "primary_number", "verified"]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["email", "primary_email", "verified"]

from rest_framework import serializers

from accounts.models import Student, User, PhoneNumberModel, Email


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
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

    def get_first_name(self, obj):
        if obj.preferred_name != "":
            return obj.preferred_name
        else:
            return obj.first_name


class UserSearchSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def get_first_name(self, obj):
        if obj.preferred_name != "":
            return obj.preferred_name
        else:
            return obj.first_name


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
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = PhoneNumberModel
        fields = ["phone_number", "primary_number", "verified"]

    def get_phone_number(self, obj):
        # PhoneNumberField() is an object; turns it into string
        return obj.phone_number.as_e164


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["email", "primary_email", "verified"]

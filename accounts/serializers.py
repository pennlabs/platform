from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response


from accounts.models import Email, PhoneNumberModel, Student, User
from accounts.verification import sendEmailVerification, sendSMSVerification


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
        fields = ["id", "phone_number", "primary", "verified", "verification_code"]
        read_only_fields = ["verified"]
        extra_kwargs = {"verification_code": {"write_only": True}}

    # def validate_phone_number(self, value):
    #     print("validate phone number called")
    #     print(self.context["request"].user.phone_numbers.filter(phone_number=value).count())
    #     if self.context["request"].user.phone_numbers.filter(phone_number=value).count() > 0:
    #         print("caught error")
    #         raise serializers.ValidationError("Duplicate phone number used")
    #     return super.validate_phone_number(value)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        instance = super().create(validated_data)
        instance.verified = False
        instance.primary = False
        instance.verification_code = get_random_string(length=6, allowed_chars="1234567890")
        instance.verification_timestamp = timezone.now()
        instance.save()
        sendSMSVerification(instance.phone_number, instance.verification_code)
        return instance

    def update(self, instance, validated_data):
        if "verification_code" in validated_data:
            elapsed_time = timezone.now() - instance.verification_timestamp
            if (
                validated_data["verification_code"] == instance.verification_code
                and elapsed_time.total_seconds() < User.VERIFICATION_EXPIRATION_MINUTES * 60
            ):
                if self.context["request"].user.phone_numbers.filter(verified=True).count() == 0:
                    instance.primary = True
                instance.verified = True
            elif elapsed_time.total_seconds() >= User.VERIFICATION_EXPIRATION_MINUTES * 60:
                raise serializers.ValidationError(
                    detail={"detail": "Verification code has expired"}
                )
            else:
                raise serializers.ValidationError(detail={"detail": "Incorrect verification code"})
        if "primary" in validated_data and validated_data["primary"]:
            self.context["request"].user.phone_numbers.all().update(primary=False)
            instance.primary = True
        instance.save()
        return instance


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["id", "email", "primary", "verified", "verification_code"]
        extra_kwargs = {"verification_code": {"write_only": True}}

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        instance = super().create(validated_data)
        instance.verified = False
        instance.primary = False
        instance.verification_code = get_random_string(length=6, allowed_chars="1234567890")
        instance.verification_timestamp = timezone.now()
        instance.save()
        sendEmailVerification(instance.email, instance.verification_code)
        return instance

    def update(self, instance, validated_data):
        if "verification_code" in validated_data:
            elapsed_time = timezone.now() - instance.verification_timestamp
            if (
                validated_data["verification_code"] == instance.verification_code
                and elapsed_time.total_seconds() < User.VERIFICATION_EXPIRATION_MINUTES * 60
            ):
                if self.context["request"].user.emails.filter(verified=True).count() == 0:
                    instance.primary = True
                instance.verified = True
            elif elapsed_time.total_seconds() >= User.VERIFICATION_EXPIRATION_MINUTES * 60:
                raise serializers.ValidationError(
                    detail={"detail": "Verification code has expired"}
                )
            else:
                raise serializers.ValidationError(detail={"detail": "Incorrect verification code"})
        if "primary" in validated_data and validated_data["primary"]:
            self.context["request"].user.emails.all().update(primary=False)
            instance.primary = True

        instance.save()
        return instance

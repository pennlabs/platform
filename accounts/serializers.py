from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import serializers

from accounts.mixins import ManyToManySaveMixin
from accounts.models import Email, Major, PhoneNumberModel, School, Student, User
from accounts.verification import sendEmailVerification, sendSMSVerification


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("id", "name")
        extra_kwargs = {"id": {"read_only": False}}


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ("id", "name", "degree_type")
        extra_kwargs = {"id": {"read_only": False}}


class StudentSerializer(ManyToManySaveMixin, serializers.ModelSerializer):
    major = MajorSerializer(many=True)
    school = SchoolSerializer(many=True)

    class Meta:
        model = Student
        fields = ("major", "school", "graduation_year")

        save_related_fields = ["major", "school"]


class UserSearchSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def get_first_name(self, obj):
        return obj.get_preferred_name()


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumberModel
        fields = ["id", "phone_number", "primary", "verified", "verification_code"]
        read_only_fields = ["verified"]
        extra_kwargs = {"verification_code": {"write_only": True}}

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
    student = StudentSerializer()
    emails = EmailSerializer(many=True)
    phone_numbers = PhoneNumberSerializer(many=True)

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
            "student",
            "phone_numbers",
            "emails",
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

    # Users are pulled from Penn DB, so come with no preferred
    # name. Thus, this logic only needs to happen on update.
    def update(self, instance, validated_data):
        if "get_preferred_name" in validated_data:
            instance.preferred_name = validated_data["get_preferred_name"]
            if instance.preferred_name == instance.first_name:
                instance.preferred_name = ""

            instance.save()
        if "student" in validated_data:
            # Copied from DRF UpdateModelMixin
            # https://github.com/encode/django-rest-framework/blob/master/rest_framework/mixins.py
            data = validated_data.pop("student")
            serializer = StudentSerializer(instance.student, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return instance

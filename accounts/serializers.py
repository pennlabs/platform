from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import serializers

from accounts.mixins import ManyToManySaveMixin
from accounts.models import Email, PhoneNumberModel, Student, User, Major
from accounts.verification import sendEmailVerification, sendSMSVerification


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ("name",)


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ("name",)


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

        # xyz = serializer

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
        return instance


class UserSearchSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def get_first_name(self, obj):
        return obj.get_preferred_name()


class StudentSerializer(ManyToManySaveMixin, serializers.ModelSerializer):
    # user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = ("major", "school", "graduation_year")

        # many to many fields
        save_related_fields = ["major", "school"]

'''    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop("user")
        for key in user_representation:
            if key != "pennid":
                representation[key] = user_representation[key]
        return representation'''


class UserSerializer2(serializers.ModelSerializer):
    first_name = serializers.CharField(source="get_preferred_name", required=False)
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    user_permissions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="codename"
    )
    product_permission = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="codename", source="user_permissions"
    )  # TODO: remove this once all products update to new version of DLA
    student = StudentSerializer()

    class Meta:
        model = User
        fields = ("pennid",
            "first_name",
            "last_name",
            "username",
            "email",
            "groups",
            "product_permission",
            "user_permissions",
            "student")

    def update(self, instance, validated_data):
        if "student" in validated_data:
            student_fields = validated_data.pop("student")
            student_fields.save()

        return super().update(instance, validated_data)


    '''def update(self, instance, validated_data):
        if "profile" in validated_data:
            # get profile elements
            profile_fields = validated_data.pop("profile")
            # get instance of profile
            profile = instance.profile
            # get relevante valid fields
            valid_fields = {f.name: f for f in Profile._meta.get_fields()}
            for key, value in profile_fields.items():
                if key in valid_fields:
                    field = valid_fields[key]
                    if isinstance(field, models.ManyToManyField):
                        # 
                        related_objects = getattr(profile, field.get_attname())
                        related_objects.clear()
                        for item in value:
                            related_objects.add(field.related_model.objects.get(**item))
                    else:
                        setattr(profile, key, value)
            profile.save()
        
        # pass along default update of other fields
        return super().update(instance, validated_data)'''


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

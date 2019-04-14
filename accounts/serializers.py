from rest_framework import serializers

from accounts.models import PennAffiliation, ProductPermission, Student, User


class PennAffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PennAffiliation
        fields = ('name',)


class ProductPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPermission
        fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    affiliation = PennAffiliationSerializer(read_only=True, many=True)
    product_permissions = ProductPermissionSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('uuid', 'affiliation', 'product_permissions')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = ('user', 'major', 'school')

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop('user')
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation

from rest_framework import serializers

from accounts.models import PennAffiliation, ProductPermission, Student, User


class UserSerializer(serializers.ModelSerializer):
    affiliation = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    product_permission = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
     )
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'affiliation', 'product_permission')


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

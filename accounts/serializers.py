from rest_framework import serializers

from accounts.models import Student, User


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

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'affiliation', 'product_permission')


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

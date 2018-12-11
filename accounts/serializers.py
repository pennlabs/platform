from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Student


# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password', 'name', 'school', 'major')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['email'], validated_data['password'],
#             name=validated_data['name'], school=validated_data['school'], major=validated_data['major'])
#         return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = ('user', 'name', 'major', 'school')

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop('user')
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation


# class LoginUserSerializer(serializers.Serializer):
#     email = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Unable to log in with provided credentials.")

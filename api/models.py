from django.db import models
from rest_framework import serializers

class Member(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, primary_key=True)
    bio = models.TextField()
    location = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    photo = models.URLField()
    linkedin = models.URLField()
    website = models.URLField()
    github = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('name', 'username', 'bio', 'location', 'role', 'photo', 'linkedin', 'website', 'github')

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url = models.URLField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'username', 'bio', 'location', 'role', 'photo', 'linkedin', 'website', 'github')

class Update(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    body = models.TextField()

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ('product', 'title', 'body')
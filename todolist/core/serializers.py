from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, NumericPasswordValidator
from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True, max_length=50)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        validate_password(validated_data['password'], user)
        user.set_password(user.password)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True, max_length=50)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False):
        self._password_repeat = self.initial_data.pop('password_repeat')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):

        # validate password
        if validated_data['password'] != self._password_repeat:
            raise ValidationError('Passwords must match')

        validate_password(validated_data['password'])

        # create object
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

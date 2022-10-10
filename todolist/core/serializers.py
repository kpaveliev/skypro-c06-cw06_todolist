from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = User
        fields = '__all__'

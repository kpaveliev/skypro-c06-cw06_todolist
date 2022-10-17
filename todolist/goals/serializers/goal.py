from rest_framework import serializers

from goals.models import Goal
from goals.models import Category
from core.serializers import RetrieveUpdateSerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.SlugRelatedField(
        source='category',
        many=False,
        queryset=Category.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    user = RetrieveUpdateSerializer(read_only=True)
    category = serializers.SlugRelatedField(
        source='category',
        many=False,
        queryset=Category.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
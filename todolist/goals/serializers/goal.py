from rest_framework import serializers

from goals.models import Goal
from goals.models import Category
from core.serializers import RetrieveUpdateSerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value


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
from rest_framework import serializers

from goals.models import Comment
from core.serializers import RetrieveUpdateSerializer


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = RetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
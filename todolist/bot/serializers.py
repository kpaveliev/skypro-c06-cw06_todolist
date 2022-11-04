from rest_framework import serializers

from .models import TgUser


class TgUserUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TgUser
        fields = "__all__"
        read_only_fields = ("tg_user_id", "tg_chat_id")

    def validate_verification_code(self, value):
        if not TgUser.objects.filter(user_id__isnull=True, verification_code=value).first().exists():
            raise serializers.ValidationError("Wrong verification code passed, try again")
        return value

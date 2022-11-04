from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

from .models import TgUser
from .serializers import TgUserUpdateSerializer


class TgUserUpdateView(UpdateAPIView):
    model = TgUser
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserUpdateSerializer

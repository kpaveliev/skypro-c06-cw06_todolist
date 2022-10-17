from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from goals.models import Category
from goals.serializers import CategoryCreateSerializer


class CategoryCreateView(CreateAPIView):
    model = Category
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryCreateSerializer

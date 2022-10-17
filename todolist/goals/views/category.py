from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions, filters

from goals.models import Category
from goals.serializers import CategoryCreateSerializer, CategorySerializer
from rest_framework.pagination import LimitOffsetPagination


class CategoryCreateView(CreateAPIView):
    model = Category
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    model = Category
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Category.objects.filter(
            user=self.request.user, is_deleted=False
        )

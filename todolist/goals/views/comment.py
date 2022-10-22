from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.models import Comment
from goals.serializers import CommentCreateSerializer, CommentSerializer
from goals.permissions import UserPermissions


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["created"]
    ordering = ["-created"]
    search_fields = ["goal__title"]

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user, is_deleted=False
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, UserPermissions]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user, is_deleted=False)

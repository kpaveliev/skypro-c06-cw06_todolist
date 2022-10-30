from rest_framework import permissions

from goals.models import BoardParticipant, Category


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return Category.objects.filter(
                board__participants__user=request.user
            ).exists()
        return Category.objects.filter(
            board__participants__user=request.user,
            board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()


class UserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        else:
            return obj.user == request.user

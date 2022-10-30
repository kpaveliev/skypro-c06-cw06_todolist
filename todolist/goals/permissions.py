from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):

    roles = [BoardParticipant.Role.owner]

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj
            ).exists()

        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj,
            role__in=self.roles
        ).exists()


class CategoryPermissions(BoardPermissions):
    roles = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj=obj.board)


class GoalPermissions(BoardPermissions):
    roles = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj=obj.category.board)


class UserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        else:
            return obj.user == request.user

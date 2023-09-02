from rest_framework.permissions import SAFE_METHODS, BasePermission


class CanEditOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
                request.method in SAFE_METHODS
        ) or (
                obj.author == request.user
        ) or (
                request.user.role == 'moderator'
        ) or (
                request.user.role == 'admin'
        )

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or (request.user.is_authenticated and request.user.is_admin)
        )


class AuthorOrCanEditOrReadOnly(BasePermission):

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


class CanEditOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
        ) or (
            request.user.role == 'moderator'
        ) or (
            request.user.role == 'admin'
        )


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.is_admin
        )

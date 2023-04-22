from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Админ - изменение, все -чтение"""

    def has_permission(self, request):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Админ/автору, остальные - чтение."""

    def has_object_permission(self, request, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user == obj.author)
            or request.user.is_staff
        )

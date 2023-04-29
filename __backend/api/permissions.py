from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''All rights to admin, read only to all'''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    '''All rights to admin and author, read only to all'''

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user == obj.author)
            or request.user.is_admin
            or request.user.is_superuser
        )

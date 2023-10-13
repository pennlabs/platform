from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    """
    Grants permission if the current user is a superuser.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
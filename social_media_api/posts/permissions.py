from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow read for any, write only for owner."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'author', None)
        return owner == request.user

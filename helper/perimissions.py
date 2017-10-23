from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAncestorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        ancestor = request.user.ancestor
        return (
            request.method in SAFE_METHODS
        )
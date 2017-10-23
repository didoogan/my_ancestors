from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS

from ancestors.models import Ancestor


class IsAncestorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        UNSAFE_METHODS = ('PUT', 'PATCH', 'DELETE')
        if request.method in SAFE_METHODS or request.method == 'POST' and \
                request.user and is_authenticated(request.user):
            return True
        if request.method in UNSAFE_METHODS:
            updater = request.user.ancestor
            updated = Ancestor.objects.get(id=view.kwargs.get('pk'))
            if updated in updater.ancestors.all() or updated == updater:
                return True
        return False

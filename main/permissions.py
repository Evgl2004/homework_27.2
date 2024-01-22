from rest_framework.permissions import BasePermission
from users.services import is_moderator


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        return not is_moderator(request.user)

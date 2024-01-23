from rest_framework.permissions import BasePermission
from users.services import is_moderator


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        return not is_moderator(request.user)


class IsObjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsObjectOwnerOrModerator(BasePermission):

    def has_object_permission(self, request, view, obj):
        if is_moderator(request.user):
            return True
        return request.user == obj.owner



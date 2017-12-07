from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission for object owners and admin
    """
    def has_object_permission(self, request, view, obj):
        return is_owner_or_admin(request.user, obj)


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """All permissions for owners and admins, read permissions to everybody.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to everybody
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to owners and admins.
        return is_owner_or_admin(request.user, obj)


def is_owner_or_admin(user, obj):
    """Return True if `user` is either owner of `obj` or an admin.
    """
    if user.is_staff:
        return True
    # some entites (e.g. Student) have a direct `user` attribute
    if hasattr(obj, 'user'):
        return obj.user == user
    # other entites (e.g. TaskSession) have indirect ownership through
    # `student` attribute
    if hasattr(obj, 'student'):
        return obj.student.user == user
    return False

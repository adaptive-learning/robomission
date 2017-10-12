from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission for object owners and admin
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # some entites (e.g. Student) have a direct `user` attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # other entites (e.g. TaskSession) have indirect ownership through
        # `student` attribute
        if hasattr(obj, 'student'):
            return obj.student.user == request.user
        return False

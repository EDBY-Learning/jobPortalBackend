from rest_framework import permissions

class TeacherIsOwnerRegistration(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.user == request.user
        else:
            return False

class TeacherIsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.teacher.user == request.user
        else:
            return False


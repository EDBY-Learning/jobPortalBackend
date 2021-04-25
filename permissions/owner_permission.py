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

class TeacherWriteOwnData(permissions.BasePermission):

    def has_permission(self, request, view):
        #print(getattr(request,'method',None))
        if request.user:
            if request.user.is_superuser:
                return True
            elif request.user.is_anonymous:
                return False
            else:
                print(request.user.teacher_user.id)
                print(request.data['teacher_id'])
                return request.user.teacher_user.id == request.data['teacher_id']
        else:
            return False

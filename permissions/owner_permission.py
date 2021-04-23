from rest_framework import permissions

class UserViewSetIsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj == request.user
        else:
            return False

class IsOrganizationPart(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            elif request.user.is_anonymous:
                return False
            else:
                return (obj == request.user.org_user_set.organization)
        else:
            return False

class IsOrganizationPublic(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.public
        else:
            return False

class IsOrganization_Admin(permissions.BasePermission):

    def has_permission(self, request, view):
        #print(getattr(request,'method',None))
        if request.user:
            if request.user.is_superuser:
                return True
            elif request.user.is_anonymous:
                return False
            else:
                return request.user.org_user_set.user_info.is_admin
        else:
            return False

class IsSelfData_forOrganizationBasicInfo(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return request.user == obj.user
        else:
            return False
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated 
from rest_framework import mixins
from rest_framework.views import APIView
from django.core import serializers as djangoSerializer
from .serializers import (
    TeacherBasicInfoSerializer,
    TeacherEducationSerializer,
    TeacherQualificationSerializer,
    TeacherExperienceSerializer,
    TeacherLanguageSerializer,
    TeacherPreferenceSerializer
)
from .models import (
    TeacherBasicInfo,
    TeacherEducation,
    TeacherExperience,
    TeacherLanguage,
    TeacherQualifications,
    TeacherPreference)

from utils.operations import update_with_partial, update_with_partial_teacher
from permissions import manage_permissions as perm 
from permissions import owner_permission as owner 

OPERATION_AFTER_LOGIN_PERMISSION = {'create': [IsAuthenticated],
                                    'retrieve':[IsAuthenticated & owner.TeacherIsOwner],
                                    'update': [IsAuthenticated],
                                    'partial_update':[IsAuthenticated]}

class TeacherRegistrationViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = TeacherBasicInfoSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[IsAuthenticated  & owner.TeacherIsOwnerRegistration  ],
                                    'update': [IsAuthenticated & owner.TeacherIsOwnerRegistration ],
                                    'partial_update':[IsAuthenticated & owner.TeacherIsOwnerRegistration]}
    queryset = TeacherBasicInfo.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

class TeacherEducationViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = TeacherEducationSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
    queryset = TeacherEducation.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

class TeacherQualificationViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = TeacherQualificationSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
    queryset = TeacherQualifications.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

class TeacherExperienceViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = TeacherExperienceSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
    queryset = TeacherExperience.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

class TeacherLanguageViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = TeacherLanguageSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
    queryset = TeacherLanguage.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

class TeacherPreferenceViewset(
    #mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = TeacherPreferenceSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
    queryset = TeacherPreference.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(teacher=request.user.teacher_user)
        serializer = self.get_serializer(instance[0])
        return Response(serializer.data)
        

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial_teacher(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

from .serializers import TeacherProfileSerializer

class TeacherProfileViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = TeacherProfileSerializer
    queryset = TeacherBasicInfo.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        instance = self.get_object()
        serializer = self.get_serializer({
            'teacher':instance,
            'education':TeacherEducation.objects.filter(teacher=instance),
            'qualification':TeacherQualifications.objects.filter(teacher=instance),
            'experience':TeacherExperience.objects.filter(teacher=instance),
            'language':TeacherLanguage.objects.filter(teacher=instance),
            'preference':TeacherPreference.objects.filter(teacher=instance)
            })
        return Response(serializer.data,status=200)
    
    
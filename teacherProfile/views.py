from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated#, IsOwnerOrReject 
from rest_framework import mixins
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import (
    TeacherBasicInfoSerializer,
    TeacherEducationSerializer,
    TeacherQualificationSerializer,
    TeacherExperienceSerializer,
    TeacherLanguageSerializer
)
from .models import (
    TeacherBasicInfo,
    TeacherEducation,
    TeacherExperience,
    TeacherLanguage,
    TeacherQualifications,
    SubjectLookingFor,
    PositionLookingFor)

from utils.operations import update_with_partial
from permissions import manage_permissions as perm 

class TeacherRegistrationViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = TeacherBasicInfoSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[AllowAny],
                                    'update': [AllowAny],
                                    'partial_update':[AllowAny]}
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

class TeacherEducationViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = TeacherEducationSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[AllowAny],
                                    'update': [AllowAny],
                                    'partial_update':[AllowAny]}
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

class TeacherQualificationViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = TeacherQualificationSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[AllowAny],
                                    'update': [AllowAny],
                                    'partial_update':[AllowAny]}
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

class TeacherExperienceViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = TeacherExperienceSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[AllowAny],
                                    'update': [AllowAny],
                                    'partial_update':[AllowAny]}
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

class TeacherLanguageViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = TeacherLanguageSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[AllowAny],
                                    'update': [AllowAny],
                                    'partial_update':[AllowAny]}
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

class TeacherLookingForSubjects(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        return Response("UP",status=200)
    
    def post(self,request,format=None):
        return Response("UP",status=200)

class TeacherLookingForPositions(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        return Response("UP",status=200)
    
    def post(self,request,format=None):
        return Response("UP",status=200)

class TeacherLookingForCountry(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        return Response("UP",status=200)
    
    def post(self,request,format=None):
        return Response("UP",status=200)
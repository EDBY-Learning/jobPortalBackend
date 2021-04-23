from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated#, IsOwnerOrReject 
from permissions.owner_permission import (
    IsOrganizationPublic,
    IsOrganizationPart,
    IsOrganization_Admin,
    IsSelfData_forOrganizationBasicInfo
    )
from rest_framework import mixins
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import (
    OrganizationSerializer,
    OrganizationMemberSerializer
)
from .models import ( 
    Organization,
    UserInfo,
    OrganizationMember)
from permissions import manage_permissions as utils 
from utils.operations import update_with_partial



class OrganizationViewSet(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    serializer_class = OrganizationSerializer
    permission_classes_by_action = {'retrieve':[IsOrganizationPublic | (IsAuthenticated & IsOrganizationPart)]}
    queryset = Organization.objects.all()
    def get_permissions(self):
        return utils.get_custom_permissions(self)

class CreateOrgMemberViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    serializer_class = OrganizationMemberSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[IsAuthenticated & IsSelfData_forOrganizationBasicInfo],
                                    'update': [IsAuthenticated & IsOrganization_Admin],
                                    'partial_update':[IsAuthenticated & IsOrganization_Admin]}
    queryset = OrganizationMember.objects.all()
    def get_permissions(self):
        return utils.get_custom_permissions(self)

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

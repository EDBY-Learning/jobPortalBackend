from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated#, IsOwnerOrReject 
from permissions.owner_permission import UserViewSetIsOwner
from rest_framework import mixins
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import ChangePasswordSerialier, ChangeForgetPasswordSerialier
from email_sender.views import createResetMail

class ChangePasswordViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = ChangePasswordSerialier
    permission_classes_by_action = {'create': [IsAuthenticated]}
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

class ForgetPasswordView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self,request):
        if request.data['username'] == None:
            return Response("Please provide username", status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(username=request.data['username'])
        except Exception as e:
            return Response("No user of this name", status=status.HTTP_404_NOT_FOUND)

        if user is not None:
            p0 = PasswordResetTokenGenerator()
            tk1 = p0.make_token(user)
            try:
                createResetMail(user.email,tk1)
            except Exception as e:
                return Response("Some problem with server check after 12-24 hours", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response("Please check your mail in 30-60 min", status=status.HTTP_200_OK)
        else:
            return Response("No user of this name", status=status.HTTP_404_NOT_FOUND) 


class ChangeForgetPasswordViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = ChangeForgetPasswordSerialier
    permission_classes = [AllowAny]
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
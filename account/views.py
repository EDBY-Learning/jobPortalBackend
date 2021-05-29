from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated#, IsOwnerOrReject 
from rest_framework import mixins
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import ChangePasswordSerialier, ChangeForgetPasswordSerialier
from email_sender.views import createResetMail
from .models import ForgotPasswordData

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
        if request.data['email'] == None:
            return Response("Please provide email", status=status.HTTP_404_NOT_FOUND)
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
                data = ForgotPasswordData.objects.get_or_create(mobile=request.data['username'],email=request.data['email'])
                createResetMail(request.data['username'],request.data['email'],tk1)
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

class SaveForgotPasswordData(APIView):
    permission_classes = [AllowAny]

    def post(self,request,format=None):
        mobile = request.POST.get('mobile',None)
        email = request.POST.get('email',None)

        if (not mobile) and (not email):
             Response(data={'message':'Please provide both email and mobile'},status=status.HTTP_400_BAD_REQUEST)
        data = ForgotPasswordData.objects.create(mobile=mobile,email=email)

        return Response("Succesfully data sent to admin, please have patience we will respond soon",status=status.HTTP_200_OK)

# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token

# class AdminTokenObtainPairView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         if user.is_staff:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'token': token.key,
#                 'user_id': user.pk,
#                 'email': user.email
#             })
#         else:
#             return Response("Only Admin User are allowed", status=status.HTTP_401_UNAUTHORIZED)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if not user.is_staff:
            raise serializers.ValidationError("Only Admin User are allowed!!")
        token = super().get_token(user)
        return token

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
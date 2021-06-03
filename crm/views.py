from rest_framework.response import Response
from crm.models import CustomFCMDevice, FCMClickRate, PassKeyNotifications
from crm.serializers import CustomAuthFCMDeviceSerializer, CustomFCMDeviceSerializer

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from fcm_django.api.rest_framework import DeviceViewSetMixin

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.utils.crypto import get_random_string

class CustomFCMDeviceCreateOnlyViewSet(DeviceViewSetMixin, CreateModelMixin, GenericViewSet):
    queryset = CustomFCMDevice.objects.all()
    serializer_class = CustomFCMDeviceSerializer

class CustomAuthFCMDeviceViewSet(DeviceViewSetMixin, ModelViewSet):
    queryset = CustomFCMDevice.objects.all()
    serializer_class = CustomAuthFCMDeviceSerializer

class CustomAuthorizedMixin(object):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        # filter all devices to only those belonging to the current user
        return self.queryset.filter(user=self.request.user)

class CustomFCMDeviceAuthorizedViewSet(CustomAuthorizedMixin, CustomAuthFCMDeviceViewSet):
    pass

class JobsNotification(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get_query_param(self,num,whom):
        key =  get_random_string(12)
        temp = FCMClickRate.objects.create(
            query_param=key,
            notification_sent=num,
            whom=whom)
        return key

    def get_url(self,URL,trackkey):
        if "?" in URL:
            return URL+"track_key="+trackkey
        else:
            return URL+"?track_key="+trackkey

    def all_teachers(self,title,message,url,whom):
        # devices  = CustomFCMDevice.objects.filter(active=True).all()  
        devices  = CustomFCMDevice.objects.all()
        key = self.get_query_param(len(devices),whom)
        devices.send_message(title=title, body=message, click_action=self.get_url(url,key))
        return Response("Sent to "+str(len(devices)),status=200)

    def registered_teachers(self,title,message,url,whom):
        devices  = CustomFCMDevice.objects.filter(user__isnull=False,active=True).all()  
        key = self.get_query_param(len(devices),whom)
        devices.send_message(title=title, body=message, click_action=self.get_url(url,key))
        return Response("Sent to "+str(len(devices)),status=200)

    def unregistered_teacher(self,title,message,url,whom):
        devices  = CustomFCMDevice.objects.filter(user__isnull=True,active=True).all()  
        key = self.get_query_param(len(devices),whom)
        devices.send_message(title=title, body=message, click_action=self.get_url(url,key))
        return Response("Sent to "+str(len(devices)),status=200)

    def post(self,request,format=None):
        passkey = request.data.get('passkey',None)
        whom = request.data.get('whom',None)
        if (not passkey) or (not whom):
            return Response("Unauthorized provide passkey",status=403)
        verifiation_token = PassKeyNotifications.objects.get(whom=whom)
        if not verifiation_token:
            return Response("Unauthorized wrong target user",status=403)
        if (verifiation_token.passkey != passkey):
            return Response("Unauthorized wrong passkey",status=403)

        title = request.data.get('title',None)
        message = request.data.get('message',None)
        url = request.data.get('url',None)

        if (not title) or (not message) or (not url):
            return Response("Provide title, message and url",status=402)
        if whom=='all':
            return self.all_teachers(title,message,url,whom)
        if whom=='registered':
            return self.registered_teachers(title,message,url,whom)
        if whom=='unregistered':
            return self.unregistered_teacher(title,message,url,whom)
        
        return Response("Bad Request",status=400)

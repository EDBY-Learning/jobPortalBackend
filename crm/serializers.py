from fcm_django.api.rest_framework import DeviceViewSetMixin, UniqueRegistrationSerializerMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import (
                ClickCRM, CustomFCMDevice,SearchCRM)

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate 
from utils.validations import check_password_length
import re
from django.db.utils import IntegrityError
from utils.operations import generate_random_hash

MOBILE_REGEX = re.compile("^[0-9]*$")
CREATE_ORG_REQUEST = 'POST'
ADD_MEMBER_ORG_REQUEST = set({'PUT','PATCH'})

class CustomDeviceSerializerMixin(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id","name", "registration_id", "device_id", "active",
            "date_created", "type"
        )
        read_only_fields = ("date_created",)

        extra_kwargs = {"active": {"default": True}}

class CustomFCMDeviceSerializer(serializers.ModelSerializer, UniqueRegistrationSerializerMixin):
    class Meta(CustomDeviceSerializerMixin.Meta):
        model = CustomFCMDevice

        extra_kwargs = {"id": {"read_only": True, "required": False}}
        extra_kwargs.update(CustomDeviceSerializerMixin.Meta.extra_kwargs)

class CustomAuthFCMDeviceSerializer(serializers.ModelSerializer, UniqueRegistrationSerializerMixin):
    class Meta(CustomDeviceSerializerMixin.Meta):
        model = CustomFCMDevice

        extra_kwargs = {
            "id": {"read_only": True, "required": False}
            }
        extra_kwargs.update(CustomDeviceSerializerMixin.Meta.extra_kwargs)
    
    def create(self, validated_data):
        request = self.context.get('request',None)
        customDevice,created = CustomFCMDevice.objects.update_or_create(registration_id=validated_data['registration_id'],defaults=validated_data)
        customDevice.user = request.user
        customDevice.save()
        return customDevice



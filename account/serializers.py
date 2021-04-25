from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import authenticate
from email_sender.views import createWelcomeMail
from utils.validations import check_password_length
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.utils import IntegrityError

class ChangePasswordSerialier(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    class Meta:
        fields = ['username','password', 'new_password', 'confirm_password']
        extra_kwargs = {
            'username': {'required': True},
            'confirm_password': {'required': True},
            'new_password': {'required': True},
            'password': {'required': True}}
    
    def validate_new_password(self,new_password):
        return check_password_length(new_password)

    def validate(self, data):
        if (data['new_password'] == data['password']):
            raise serializers.ValidationError("New password should be different than current password!") 
        elif (data['new_password'] == data['confirm_password']):
            return data
        raise serializers.ValidationError("Password doesn't match!") 

    def create(self,validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user is not None:
            user.set_password(validated_data['new_password'])
            user.save()
            return user
        else:
            raise serializers.ValidationError("Wrong Username and Password! No authentication!")

class ChangeForgetPasswordSerialier(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    token = serializers.CharField(write_only=True)
    class Meta:
        fields = ['username', 'new_password', 'confirm_password','token']
        extra_kwargs = {
            'username': {'required': True},
            'confirm_password': {'required': True},
            'new_password': {'required': True},
            'token': {'required': True}}
    
    def validate_new_password(self,new_password):
        return check_password_length(new_password)

    def validate(self, data):
        if (data['new_password'] == data['confirm_password']):
            return data
        raise serializers.ValidationError("Password doesn't match!") 

    def create(self,validated_data):
        try:
            user = User.objects.get(username=validated_data['username'])
        except IntegrityError as e:
            raise serializers.ValidationError("Wrong Username!")
        if user is not None:
            p0 = PasswordResetTokenGenerator()
            if p0.check_token(user,validated_data['token']):
                user.set_password(validated_data['new_password'])
                user.save()
                return user
            else:
                raise serializers.ValidationError("Wrong Token! No authentication!")
        else:
            raise serializers.ValidationError("Wrong Username! No authentication!")
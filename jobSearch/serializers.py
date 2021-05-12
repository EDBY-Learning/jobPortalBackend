from jobPortal.models import (
    JobInfo,
    JobSearch,
    JobPostByOutSider,
    FeedbackByUser
)

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate 
from utils.validations import check_password_length
import re
from django.db.utils import IntegrityError
from utils.operations import generate_random_hash

MOBILE_REGEX = re.compile("^[0-9]*$")
# CREATE_ORG_REQUEST = 'POST'
# ADD_MEMBER_ORG_REQUEST = set({'PUT','PATCH'})

class FeedbackByUserSerializer(serializers.ModelSerializer):
    usernamefake = serializers.CharField(read_only=True)
    class Meta:
        model = FeedbackByUser
        fields = "__all__"
        
    def validate_feedback(self,feedback):
        if feedback.strip()=="":
            raise serializers.ValidationError("Feedback can't be empty!")
        return feedback

    def create(self,validated_data):
        request = self.context.get('request',None)
        feedback = FeedbackByUser.objects.create(usernamefake=request.user,**validated_data)
        return feedback

class JobInfoSerializer(serializers.ModelSerializer):
    entry_time = serializers.CharField(read_only=True)
    isByEdby = serializers.CharField(read_only=True)
    class Meta:
        model = JobInfo
        fields = "__all__"
        required_fields = ["city"]

class JobPostByOutsiderSerializer(serializers.ModelSerializer):
    entry_time = serializers.CharField(read_only=True)
    is_published = serializers.CharField(read_only=True)
    class Meta:
        model = JobPostByOutSider
        fields = "__all__"
        
    def validate_school(self,school):
        if school.strip()=="":
            raise serializers.ValidationError("School can't be empty!")
        return school

    def validate_city(self,city):
        if city.strip()=="":
            raise serializers.ValidationError("City can't be empty!")
        return city

    def validate_positions(self,positions):
        if positions.strip()=="":
            raise serializers.ValidationError("Designation can't be empty!")
        return positions

    def validate(self,data):
        if data['contact'].strip()==""  and data['email'].strip()=="":
            raise serializers.ValidationError("Email or contact number should be provided")
        return data

class JobPostByEdbySerializer(serializers.ModelSerializer):
    entry_time = serializers.CharField(read_only=True)
    is_published = serializers.CharField(read_only=True)
    class Meta:
        model = JobInfo
        fields = "__all__"
        
    def validate_subjects(self,subjects):
        if subjects.strip()=="":
            raise serializers.ValidationError("Subjects can't be empty!")
        return subjects

    def validate_city(self,city):
        if city.strip()=="":
            raise serializers.ValidationError("City can't be empty!")
        return city

    def validate_positions(self,positions):
        if positions.strip()=="":
            raise serializers.ValidationError("Designation can't be empty!")
        return positions

    def validate(self,data):
        return data
       

    


# class UserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInfo
#         fields = ("mobile","country","is_admin","is_employee")
#     def get_fields(self,*args,**kwargs):
#         fields = super(UserInfoSerializer,self).get_fields(*args,**kwargs)
#         request = self.context.get('request',None)
#         if request and (getattr(request,'method',None) == CREATE_ORG_REQUEST):
#             fields['is_employee'].read_only = True
#             fields['is_admin'].read_only = True
#         return fields

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User 
#         fields = ['first_name','email','password','confirm_password']
#         extra_kwargs = {
#         'password': {'required': True},
#         'confirm_password': {'required': True}}
    
#     def validate(self,data):
#         if (data['password'] == data['confirm_password']):
#             data.pop('confirm_password')
#             data['username'] = data['email']
#             return data 
#         raise serializers.ValidationError("Password doesn't match!")
#     def validate_email(self,email):
#         if email.strip()=="":
#             raise serializers.ValidationError("Email can't be empty!")
#         return email
#     def validate_first_name(self,first_name):
#         if first_name.strip()=="":
#             raise serializers.ValidationError("Name can't be empty!")
#         return first_name
#     def validate_password(self,password):
#         return check_password_length(password)

# class OrganizationMemberSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=True)
#     organization = OrganizationSerializer(read_only=True)
#     user_info = UserInfoSerializer(required=True)
#     id = serializers.CharField(read_only=True)
#     class Meta:
#         model = OrganizationMember
#         fields = ['user','user_info',"organization",'id']
        
#     def validate(self,data):
#         request = self.context.get('request',None)
#         if request and (getattr(request,'method',None) == CREATE_ORG_REQUEST):
#             data['user_info']['is_admin'] = True
#         return data 

#     def validate_mobile(self,mobile):
#         if not MOBILE_REGEX.match(mobile):
#             raise serializers.ValidationError("Mobile Number should be only numeric")
#         return mobile

#     def createUser(self,data):
#         user = User.objects.create(**data)
#         user.set_password(data['password'])
#         user.save()
#         return user

#     def create(self,validated_data):
#         try:
#             user = self.createUser(validated_data.pop('user'))
#         except IntegrityError as e:
#             raise serializers.ValidationError("Email already used for registration!!")
#         orgData = validated_data.pop("organization")
#         org = Organization.objects.create(**orgData)
#         user_info = UserInfo.objects.create(**validated_data['user_info'])
#         member = OrganizationMember.objects.create(user=user,organization=org ,user_info=user_info)
#         return member

#     def update(self,instance,validated_data):
#         user = self.createUser(validated_data.pop('user'))
#         org = Organization.objects.get(pk=instance.organization.id)
#         user_info = UserInfo.objects.create(**validated_data['user_info'])
#         member = OrganizationMember.objects.create(user=user,organization=org ,user_info=user_info)
#         return member

#     def get_fields(self,*args,**kwargs):
#         fields = super(OrganizationMemberSerializer,self).get_fields(*args,**kwargs)
#         request = self.context.get('request',None)
#         if request and (getattr(request,'method',None) == CREATE_ORG_REQUEST):
#             fields['organization'].read_only = False
#             fields['organization'].required = True
#         return fields


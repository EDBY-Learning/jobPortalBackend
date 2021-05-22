from jobPortal.models import (
    JobInfo,
    JobPostByOutSider,
    FeedbackByUser,
    AdminJobPost
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
       
class AdminJobPostSerializer(serializers.ModelSerializer):
    entry_time = serializers.CharField(read_only=True)
    isByEdby = serializers.CharField(read_only=True)
    class Meta:
        model = AdminJobPost
        fields = "__all__"
    
    def validate_school(self,school):
        if school.strip()=="":
            raise serializers.ValidationError("School can't be empty!")
        return school

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
    


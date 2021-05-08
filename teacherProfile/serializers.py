from .models import (
    TeacherBasicInfo,
    TeacherEducation,
    TeacherExperience,
    TeacherLanguage,
    TeacherQualifications,
    TeacherPreference)
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate 
from utils.validations import check_password_length
import re
from django.db.utils import IntegrityError

MOBILE_REGEX = re.compile("^[0-9]*$")
YEAR_REGEX = re.compile("^[0-9]{4}$")
REGISTER_TEACHER_REQUEST = "POST"
UPDATE_TEACHER_BASIC_INFO_REQUEST = set({'PUT','PATCH'})

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User 
        fields = ['first_name','password','confirm_password']
        extra_kwargs = {
        'first_name':{'required':True},
        'password': {'required': True},
        'confirm_password': {'required': True}}
    
    def validate(self,data):
        if (data['password'] == data['confirm_password']):
            data.pop('confirm_password')
            return data 
        raise serializers.ValidationError("Password doesn't match!")
    
    def validate_first_name(self,first_name):
        if first_name.strip()=="":
            raise serializers.ValidationError("Name can't be empty!")
        return first_name
    def validate_password(self,password):
        return check_password_length(password)

class TeacherBasicInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = TeacherBasicInfo
        fields = ('id','user',"country_code","mobile","country","description","dob","email")
        required_fields = ["country_code","mobile","country","email"]
    
    def createUser(self,data,mobile):
        user = User.objects.create(**data,username=mobile)
        user.set_password(data['password'])
        user.save()
        return user
    
    def validate(self,data):
        return data 
    
    def validate_email(self,email):
        return email
    
    def validate_mobile(self,mobile):
        if not MOBILE_REGEX.match(mobile) or mobile.strip()=="":
            raise serializers.ValidationError("Mobile Number should be only numeric")
        return mobile
    
    def create(self,validated_data):
        try:
            user = self.createUser(validated_data.pop('user'),validated_data['mobile'])
        except IntegrityError as e:
            raise serializers.ValidationError("Mobile already in use")
        teacher = TeacherBasicInfo.objects.create(user=user,**validated_data)
        preference = TeacherPreference.objects.create(country=validated_data['country'],teacher=teacher,position="Teacher,Nurse",subject="English,Maths")
        return teacher
    
    def get_fields(self,*args,**kwargs):
        fields = super(TeacherBasicInfoSerializer,self).get_fields(*args,**kwargs)
        request = self.context.get('request',None)
        if request and (getattr(request,'method',None) in UPDATE_TEACHER_BASIC_INFO_REQUEST):
            fields['user'].read_only = True
            fields['mobile'].read_only = True
            fields['email'].read_only = True
            fields['country_code'].read_only = True
        return fields

class TeacherEducationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = TeacherEducation
        exclude  = ('teacher',)
        required_fields = ['degree','institute_name','start_year','end_year','score']
    
    def validate_year(self,year):
        if not YEAR_REGEX.match(year):
            raise serializers.ValidationError("Year should be just 4 digit")
        return year

    def validate_start_year(self,start_year):
        return self.validate_year(start_year)
    
    def validate_end_year(self,start_year):
        return self.validate_year(start_year)
    
    def create(self,validated_data):
        request = self.context.get('request',None)
        education = TeacherEducation.objects.create(teacher=request.user.teacher_user,**validated_data)
        return education

    def update(self,instance,validated_data):   
        education,created = TeacherEducation.objects.update_or_create(id=instance.id,defaults=validated_data)
        return education

class TeacherQualificationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = TeacherQualifications
        exclude  = ('teacher',)
        required_fields = ['degree','major_subject','start_date','end_date','score']
    
    def create(self,validated_data):
        request = self.context.get('request',None)
        qualification = TeacherQualifications.objects.create(teacher=request.user.teacher_user,**validated_data)
        return qualification

    def update(self,instance,validated_data):    
        qualification,created = TeacherQualifications.objects.update_or_create(id=instance.id,defaults=validated_data)
        return qualification

class TeacherExperienceSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = TeacherExperience
        exclude  = ('teacher',)
        required_fields = ['institute','ongoing','start_year','end_year','subjects','classes']
    
    def create(self,validated_data):
        request = self.context.get('request',None)
        experience = TeacherExperience.objects.create(teacher=request.user.teacher_user,**validated_data)
        return experience

    def update(self,instance,validated_data):    
        experience,created = TeacherExperience.objects.update_or_create(id=instance.id,defaults=validated_data)
        return experience

class TeacherLanguageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = TeacherLanguage
        exclude  = ('teacher',)
        required_fields = ['language','can_write','can_read','can_speak','can_teach']
    
    def create(self,validated_data):
        request = self.context.get('request',None)
        language = TeacherLanguage.objects.create(teacher=request.user.teacher_user,**validated_data)
        return language

    def update(self,instance,validated_data):    
        language,created  = TeacherLanguage.objects.update_or_create(id=instance.id,defaults=validated_data)
        return language

class TeacherPreferenceSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = TeacherPreference
        exclude  = ('teacher',)
        required_fields = ['subject','position','location','country']
    
    # def create(self,validated_data):
    #     request = self.context.get('request',None)
    #     preference = TeacherPreference.objects.create(teacher=request.user.teacher_user,**validated_data)
    #     return preference

    def update(self,instance,validated_data):    
        preference,created  = TeacherPreference.objects.update_or_create(id=instance.id,defaults=validated_data)
        return preference

class TeacherProfileSerializer(serializers.Serializer):
    teacher = TeacherBasicInfoSerializer(read_only=True)
    education = TeacherEducationSerializer(read_only=True,many=True)
    qualification = TeacherQualificationSerializer(read_only=True,many=True)
    experience = TeacherExperienceSerializer(read_only=True,many=True)
    language = TeacherLanguageSerializer(read_only=True,many=True)
    preference = TeacherPreferenceSerializer(read_only=True,many=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        fields = [
            'teacher','education',
            'qualification','experience',
            'language','preference']

class TeacherPublicProfileSerializer(serializers.Serializer):
    teacher = TeacherBasicInfoSerializer(read_only=True)
    education = TeacherEducationSerializer(read_only=True,many=True)
    qualification = TeacherQualificationSerializer(read_only=True,many=True)
    experience = TeacherExperienceSerializer(read_only=True,many=True)
    language = TeacherLanguageSerializer(read_only=True,many=True)
    preference = TeacherPreferenceSerializer(read_only=True,many=True)
    class Meta:
        fields = [
            'teacher','education',
            'qualification','experience',
            'language','preference']
        exclude = ('id',)

 
    
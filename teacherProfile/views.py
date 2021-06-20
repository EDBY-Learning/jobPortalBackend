from email_sender.models import MAIL_TYPE, MailRequest
from django.contrib import admin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated 
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.views import APIView
from django.core import serializers as djangoSerializer
from . import serializers as myserializer
from .models import (
    TeacherAppliedAdminJob,
    TeacherBasicInfo,
    TeacherEducation,
    TeacherExperience,
    TeacherLanguage,
    TeacherQualifications,
    TeacherPreference,
    TeacherBookmarkedJob)
from jobPortal.models import (
    AdminJobPost,
    JobInfo
)

from django.db.utils import IntegrityError
from utils.operations import update_with_partial, update_with_partial_teacher
from permissions import manage_permissions as perm 
from permissions import owner_permission as owner 

OPERATION_AFTER_LOGIN_PERMISSION = {'create': [IsAuthenticated],
                                    'retrieve':[IsAuthenticated & owner.TeacherIsOwner],
                                    'update': [IsAuthenticated & owner.TeacherIsOwner],
                                    'partial_update':[IsAuthenticated & owner.TeacherIsOwner],
                                    'destroy':[IsAuthenticated & owner.TeacherIsOwner]}

class TeacherRegistrationViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = myserializer.TeacherBasicInfoSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'retrieve':[IsAuthenticated  & owner.TeacherIsOwnerRegistration  ],
                                    'update': [IsAuthenticated & owner.TeacherIsOwnerRegistration ],
                                    'partial_update':[IsAuthenticated & owner.TeacherIsOwnerRegistration]}
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

class TeacherEducationViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    serializer_class = myserializer.TeacherEducationSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
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

class TeacherQualificationViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = myserializer.TeacherQualificationSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
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

class TeacherExperienceViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    serializer_class = myserializer.TeacherExperienceSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
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

class TeacherLanguageViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    serializer_class = myserializer.TeacherLanguageSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
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

class TeacherPreferenceViewset(
    #mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    serializer_class = myserializer.TeacherPreferenceSerializer
    permission_classes_by_action = OPERATION_AFTER_LOGIN_PERMISSION
    queryset = TeacherPreference.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(teacher=request.user.teacher_user)
        serializer = self.get_serializer(instance[0])
        return Response(serializer.data)
        

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial_teacher(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

class TeacherProfileViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = myserializer.TeacherProfileSerializer
    queryset = TeacherBasicInfo.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        instance = request.user.teacher_user
        serializer = self.get_serializer({
            'teacher':instance,
            'education':instance.teacher_education,
            'qualification':instance.teacher_qualification,
            'experience':instance.teacher_experience,
            'language':instance.teacher_language,
            'preference':instance.teacher_prefernce
            })
        return Response(serializer.data,status=200)

class TeacherBasicProfileViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = myserializer.TeacherBasicProfileSerializer
    queryset = TeacherBasicInfo.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        serializer = self.get_serializer({
            'teacher':request.user.teacher_user
            })
        return Response(serializer.data,status=200)

# from rest_framework.throttling import UserRateThrottle
class TeacherPublicProfileViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    # throttle_classes = [UserRateThrottle]
    serializer_class = myserializer.TeacherPublicProfileSerializer
    queryset = TeacherBasicInfo.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        instance = self.get_object()
        serializer = self.get_serializer({
            'teacher':instance,
            'education':instance.teacher_education,
            'qualification':instance.teacher_qualification,
            'experience':instance.teacher_experience,
            'language':instance.teacher_language,
            'preference':instance.teacher_prefernce
            })
        return Response(serializer.data,status=200)
    
class BookmarkJobViewset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        teacher =  request.user.teacher_user
        jobId = request.GET.get('jobID','')
        try:
            job = JobInfo.objects.get(pk=jobId)
        except IntegrityError as e:
            raise serializers.ValidationError("Wrong Id!")
        bookmark,_ = TeacherBookmarkedJob.objects.update_or_create(teacher=teacher,job=job)
        return Response(bookmark.job.to_dict(),status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        #BUG: Solved
        teacher =  request.user.teacher_user
        bookmark = TeacherBookmarkedJob.objects.get(teacher=teacher,job=JobInfo.objects.get(pk=pk))  
        bookmark.delete()
        return Response(bookmark.job.to_dict(),status=status.HTTP_200_OK)

class ApplyForAdminJobViewset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        teacher =  request.user.teacher_user
        jobId = request.GET.get('jobID','')
        try:
            job = AdminJobPost.objects.get(pk=jobId)
        except IntegrityError as e:
            raise serializers.ValidationError("Wrong Id!")
        jobApplication,_ = TeacherAppliedAdminJob.objects.update_or_create(teacher=teacher,job=job)
        return Response(jobApplication.job.to_dict_confedential(),status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        teacher =  request.user.teacher_user
        prefernce = teacher.teacher_prefernce
        jobs = teacher.teacher_applied_admin_jobs.all()
        all_jobs = [{**job.job.to_dict_confedential(),"status":job.status}  for job in jobs if job.job.country==prefernce.country]
        return Response({'data':all_jobs},status=status.HTTP_200_OK)

class FetchTeacherAppliedForJob(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = myserializer.FetchTeacherAppliedForJobSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = TeacherAppliedAdminJob.objects.all()
    pagination_class = None

class TeacherList(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self,request,format=None):
        # teachers = TeacherBasicInfo.objects.all().order_by("user__date_joined")
        # teachers_list = [teacher.to_dict() for teacher in teachers]
        return Response({
            'data':[{
                'name':"NA",
                "date_joined":"NA",
                'mobile':"NA",
                'email':"NA",
                'country':"NA"
                }]},
            status=status.HTTP_200_OK)

class MailDataView(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self,request,format=None):
        mail_requests = MailRequest.objects.filter(mail_type=2).all().order_by("-entry_time")
        mail_list = [mail.to_dict() for mail in mail_requests]
        return Response({'data':mail_list},status=status.HTTP_200_OK)
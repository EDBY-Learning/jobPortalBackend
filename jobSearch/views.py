from crm.models import SearchCRM
from django.shortcuts import render
from rest_framework import response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from jobPortal.models import (
    JobInfo,
    JobPostByOutSider,
    FeedbackByUser,
    AdminJobPost
)
from .serializers import (
    FeedbackByUserSerializer,
    JobInfoSerializer,
    JobPostByOutsiderSerializer,
    JobPostByEdbySerializer
)
from teacherProfile.models import (
    TeacherPreference,
    TeacherBookmarkedJob
)
from rest_framework import status
from rest_framework import viewsets
from permissions import manage_permissions as perm 
from rest_framework import mixins
from utils.operations import update_with_partial
from operator import and_, or_
from functools import reduce
from django.db.models import Q
import re

# Create your views here.
class JobSearchResult(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request,format=None):
        # locations = request.GET.get('location','').split(',')
        # subjects = request.GET.get('subject','').split(',')
        # positions = request.GET.get('position','').split(',')
        raw_location = request.GET.get('location','').lower()
        locations = re.split('\s |, |;',raw_location)
        raw_subject = request.GET.get('subject','').lower()
        subjects = re.split('\s |, |;',raw_subject)
        raw_position = request.GET.get('position','').lower()
        positions = re.split('\s |, |;',raw_position)
        
        if not locations:
            return Response(data={'message':'Please pass location in request'},status=status.HTTP_412_PRECONDITION_FAILED)
        
        pos_q = reduce(or_,[Q(positions__icontains=position) for position in positions])
        sub_q = reduce(or_,[Q(subjects__icontains=subject) for subject in subjects])
        loc_q = reduce(or_,[Q(city__icontains=location) for location in locations])
        final_q = reduce(and_,[pos_q,sub_q,loc_q])
        jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
        all_jobs = [job.to_dict() for job in jobs[:100]]
        if len(all_jobs)>0:
            #print('here 1:',len(all_jobs))
            crm = SearchCRM.objects.update_or_create(city=raw_location,positions=raw_position,subjects=raw_subject,defaults={
                "result_count":len(all_jobs)
            })
            # crm = SearchCRM.objects.create(city=raw_location,positions=raw_position,subjects=raw_subject,result_count=len(all_jobs))
            return Response(all_jobs,status=status.HTTP_200_OK)
        else:
            final_q = reduce(or_,[pos_q,sub_q,loc_q])
            jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
            all_jobs = [job.to_dict() for job in jobs[:100]]
            #print('here 2:',len(all_jobs))
            crm = SearchCRM.objects.update_or_create(city=raw_location,positions=raw_position,subjects=raw_subject,defaults={
                "result_count":len(all_jobs)
            })
            # crm = SearchCRM.objects.create(city=raw_location,positions=raw_position,subjects=raw_subject,result_count=len(all_jobs))
            return Response(all_jobs,status=status.HTTP_200_OK)



class GetJobViaIds(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request,format=None):
        ids = request.GET.get('ids',None)
        if not ids:
            return Response(data={'message':'Please pass ids in request'},status=status.HTTP_412_PRECONDITION_FAILED)
        ids = ids.replace(" ","").split(',')
        try:
            jobs = JobInfo.objects.filter(pk__in=ids)   
        except ValueError as e:
            return Response(data={'message':'Please pass interger ids'},status=status.HTTP_412_PRECONDITION_FAILED)
        all_jobs = [job.to_dict() for job in jobs]
        return Response(all_jobs,status=status.HTTP_200_OK)

class UserFeedbackViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = FeedbackByUserSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'retrieve':[IsAuthenticated  & IsAdminUser  ],
        'list':[IsAuthenticated  & IsAdminUser  ]
    }
    queryset = FeedbackByUser.objects.all()
    def get_permissions(self):
        return perm.get_custom_permissions(self)

class JobInfoCreateEDBY(APIView):
    permission_classes = [IsAuthenticated  & IsAdminUser] 
    def post(self,request,format=None):
        # print(request.data)
        job = JobInfo.objects.create(**request.POST.dict())
        # print(job.to_dict())
        
        if len(request.FILES.keys())!=0:
            # print('here')
            key = list(request.FILES.keys())[0]
            file_handle = request.FILES[key]
            job.image = file_handle
        job.save()
        return Response("Post successful",status=status.HTTP_200_OK)

class AdminJobPostView(APIView):
    permission_classes = [IsAuthenticated  & IsAdminUser] 
    def get(self,request,format=None):
        jobs = AdminJobPost.objects.all()
        all_jobs = [job.to_dict() for job in jobs]
        return Response({'data':all_jobs},status=status.HTTP_200_OK)

    def post(self,request,format=None):
        # print(request.data)
        job = AdminJobPost.objects.create(**request.POST.dict())
        # print(job.to_dict())
        
        if len(request.FILES.keys())!=0:
            # print('here')
            key = list(request.FILES.keys())[0]
            file_handle = request.FILES[key]
            job.image = file_handle
        job.save()
        return Response("Post successful",status=status.HTTP_200_OK)

class AdminJobPostForTeacherView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        teacher =  request.user.teacher_user
        prefernce = teacher.teacher_prefernce
        cou_q = reduce(or_,[Q(country__icontains=country) for country in prefernce.country.split(',')])
        jobs = AdminJobPost.objects.filter(cou_q).all().order_by("-entry_time")
        all_jobs = [job.to_dict_confedential() for job in jobs]
        # all_jobs = [job.to_dict() for job in jobs]
        return Response({'data':all_jobs,'country':prefernce.country},status=status.HTTP_200_OK)

class JobPostByOutsideriewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = JobPostByOutsiderSerializer
    permission_classes = [AllowAny] 
    queryset = JobPostByOutSider.objects.all().order_by("-entry_time")

class LatestJobViewset(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = JobInfoSerializer
    permission_classes = [AllowAny]
    queryset = JobInfo.objects.all().order_by("-entry_time")[:15]

class GetUserDashBoardData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        teacher =  request.user.teacher_user
        prefernce = teacher.teacher_prefernce

        pos_q = reduce(or_,[Q(positions__icontains=position) for position in prefernce.position.split(",")])
        sub_q = reduce(or_,[Q(subjects__icontains=subject) for subject in prefernce.subject.split(",")])
        loc_q = reduce(or_,[Q(city__icontains=location) for location in prefernce.location.split(",")])
        cou_q = reduce(or_,[Q(city__icontains=country) for country in prefernce.country.split(',')])
        final_q = reduce(and_,[pos_q,sub_q,loc_q])
        
        jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
        all_jobs = [job.to_dict() for job in jobs]

        bookmarked_jobs = teacher.teacher_bookmarks.all().order_by("-entry_time")
        bookmarked_jobs = [job_.job.to_dict() for job_ in bookmarked_jobs]
        if len(all_jobs)>0:
            return Response({'all_jobs':all_jobs,"bookmarked_jobs":bookmarked_jobs},status=status.HTTP_200_OK)
        else:
            final_q = reduce(or_,[cou_q,loc_q])
            jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
            all_jobs = [job.to_dict() for job in jobs]
            return Response({'all_jobs':all_jobs,"bookmarked_jobs":bookmarked_jobs},status=status.HTTP_200_OK)

class GetUserSearchDashBoardData(APIView):
    permission_classes = [AllowAny]

    def get(self,request,format=None):
        teacher = None 
        authentication = False
        if request.user.is_authenticated:
            authentication = True
            try:
                teacher =  request.user.teacher_user    
            except Exception as e:
                return Response("Unexpected Error!",status=status.HTTP_409_CONFLICT) 
        
        if teacher:
            prefernce = teacher.teacher_prefernce
            pos_q = reduce(or_,[Q(positions__icontains=position) for position in prefernce.position.split(",")])
            sub_q = reduce(or_,[Q(subjects__icontains=subject) for subject in prefernce.subject.split(",")])
            loc_q = reduce(or_,[Q(city__icontains=location) for location in prefernce.location.split(",")])
            cou_q = reduce(or_,[Q(city__icontains=country) for country in prefernce.country.split(',')])
            final_q = reduce(and_,[pos_q,sub_q,loc_q])
            
            prefered_jobs = JobInfo.objects.filter(final_q).all()[:6]
            prefered_jobs = [prefered_job.to_dict() for prefered_job in prefered_jobs]
            if len(prefered_jobs)>0:
                final_q = reduce(or_,[cou_q,loc_q])
                prefered_jobs = JobInfo.objects.filter(final_q).all()[:6]
                prefered_jobs = [prefered_job.to_dict() for prefered_job in prefered_jobs]

            bookmarked_jobs = teacher.teacher_bookmarks.all()[:6]
            bookmarked_jobs = [bookmarked_job.job.to_dict() for bookmarked_job in bookmarked_jobs]
        else:
            prefered_jobs = []
            bookmarked_jobs = []
        
        recent_jobs = JobInfo.objects.all().order_by("-entry_time")[:6]
        recent_jobs = [recent_job.to_dict() for recent_job in recent_jobs]

        return Response(
            {
                'recent_jobs':recent_jobs,
                "bookmarked_jobs":bookmarked_jobs,
                "prefered_jobs":prefered_jobs,
                'authentication':{
                    'status':authentication
                }
            },
            status=status.HTTP_200_OK)


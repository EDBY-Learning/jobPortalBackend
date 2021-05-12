from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from jobPortal.models import (
    JobInfo,
    JobSearch,
    JobPostByOutSider,
    FeedbackByUser
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

# Create your views here.
class JobSearchResult(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request,format=None):
        locations = request.GET.get('location','').split(',')
        subjects = request.GET.get('subject','').split(',')
        positions = request.GET.get('position','').split(',')
        
        if not locations:
            return Response(data={'message':'Please pass location in request'},status=status.HTTP_412_PRECONDITION_FAILED)
        
        pos_q = reduce(or_,[Q(positions__icontains=position) for position in positions])
        sub_q = reduce(or_,[Q(subjects__icontains=subject) for subject in subjects])
        loc_q = reduce(or_,[Q(city__icontains=location) for location in locations])
        final_q = reduce(and_,[pos_q,sub_q,loc_q])
        jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
        all_jobs = [job.to_dict() for job in jobs]
        if len(all_jobs)>0:
            #print('here 1:',len(all_jobs))
            return Response(all_jobs,status=status.HTTP_200_OK)
        else:
            final_q = reduce(or_,[pos_q,sub_q,loc_q])
            jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
            all_jobs = [job.to_dict() for job in jobs]
            #print('here 2:',len(all_jobs))
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

class JobInfoCreateEDBYViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = JobPostByEdbySerializer
    permission_classes = [IsAuthenticated  & IsAdminUser] 
    queryset = JobInfo.objects.all().order_by("-entry_time")

    #call put with /user/id/
    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

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
        prefernce = TeacherPreference.objects.get(teacher=teacher)

        pos_q = reduce(or_,[Q(positions__icontains=position) for position in prefernce.position.split(",")])
        sub_q = reduce(or_,[Q(subjects__icontains=subject) for subject in prefernce.subject.split(",")])
        loc_q = reduce(or_,[Q(city__icontains=location) for location in prefernce.location.split(",")])
        cou_q = reduce(or_,[Q(city__icontains=country) for country in prefernce.country.split(',')])
        final_q = reduce(and_,[pos_q,sub_q,loc_q])
        
        jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
        all_jobs = [job.to_dict() for job in jobs]

        bookmarked_jobs = TeacherBookmarkedJob.objects.filter(teacher=teacher).all().order_by("-entry_time")
        bookmarked_jobs = [job_.job.to_dict() for job_ in bookmarked_jobs]
        if len(all_jobs)>0:
            return Response({'all_jobs':all_jobs,"bookmarked_jobs":bookmarked_jobs},status=status.HTTP_200_OK)
        else:
            final_q = reduce(or_,[cou_q,loc_q])
            jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
            all_jobs = [job.to_dict() for job in jobs]
            return Response({'all_jobs':all_jobs,"bookmarked_jobs":bookmarked_jobs},status=status.HTTP_200_OK)
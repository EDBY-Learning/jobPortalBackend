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
    JobPostByOutsiderSerializer
)
from rest_framework import status
from rest_framework import viewsets
from permissions import manage_permissions as perm 
from rest_framework import mixins
from utils.operations import update_with_partial

# Create your views here.
class JobSearchResult():
    pass 


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
    serializer_class = JobInfoSerializer
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
    
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
import threading


class Details(APIView):
    permission_classes = [IsAdminUser ,IsAuthenticated]#

    def get(self,request,format=None):
        num_threads = "<html><body>Number of threads running is "+str(threading.active_count())+".</body></html>"
        return HttpResponse(num_threads)

class Health(APIView):
    permission_classes = [IsAdminUser ,IsAuthenticated]#

    def get(self,request,format=None):
        return HttpResponse("UP",status=200)

# class ListCreateAPIView(mixins.ListModelMixin,
#                     mixins.CreateModelMixin,
#                     GenericAPIView):
#     """
#     Concrete view for listing a queryset or creating a model instance.
#     """
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import SignUp
from rest_framework import status
# Create your views here.

class singupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self,request,format=None):
        email = request.data.get("email",None)
        if not email:
            return Response("Please provide Email", status=status.HTTP_404_NOT_FOUND)
        SignUp.objects.update_or_create(email=email,defaults={
            "email":email
        })
        return Response("Thanks For Email, will contact you soon",status=status.HTTP_200_OK)

class demoView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self,request,format=None):
        email = request.data.get("email",None)
        name = request.data.get("name",None)
        mobile = request.data.get("mobile",None)
        if (not email) or (not name) or (not mobile):
            return Response("Please provide Email, Name and Mobile", status=status.HTTP_404_NOT_FOUND)
        SignUp.objects.update_or_create(email=email,mobile=mobile,defaults={
            "email":email,
            "name":name,
            "mobile":mobile,
            "demo":True
        })
        return Response("Thanks For Demo Registration, will contact you soon",status=status.HTTP_200_OK)
from skillDevelopment.models import PartnerCourses
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly 
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.views import APIView

# Create your views here.
class CourseList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        courses = PartnerCourses.objects.filter(active=True).all()
        all_courses  = [course.to_dict() for course in courses]
        return Response({'course':all_courses},status=status.HTTP_200_OK)



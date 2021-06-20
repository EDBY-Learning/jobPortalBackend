from django.urls import path, include
from . import views
import os

from rest_framework.routers import DefaultRouter, SimpleRouter

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()
# router.register(r'add_job_blog',views.JobBlogsViewset ,basename='add_job_blog')

urlpatterns = [
    path('',include(router.urls)),
    path('course_list/',views.CourseList.as_view())
    
]

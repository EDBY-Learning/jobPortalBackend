from django.urls import path, include
from . import views 
import os 

from rest_framework.routers import DefaultRouter, SimpleRouter

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'user_feedback',views.UserFeedbackViewset ,basename='user_feedback')
router.register(r'latest_job',views.LatestJobViewset ,basename='latest_job')
router.register(r'post_job_edby',views.JobInfoCreateEDBYViewset ,basename='latest_job')

urlpatterns = [
    path('',include(router.urls)),
    path("job_by_ids/",views.GetJobViaIds.as_view())
]
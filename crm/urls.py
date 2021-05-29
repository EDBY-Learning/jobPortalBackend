from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter
import os

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'all_devices', views.CustomFCMDeviceCreateOnlyViewSet,basename="all_devices")
router.register(r'auth_devices', views.CustomFCMDeviceAuthorizedViewSet,basename="auth_devices")

urlpatterns = [
    path('', include(router.urls)),
    path("job_notification/",views.JobsNotification.as_view()),
]

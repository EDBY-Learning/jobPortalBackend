from django.urls import path, include
from . import views
import os

from rest_framework.routers import DefaultRouter, SimpleRouter

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register(r'register_organization',views.OrganizationViewSet ,basename='register_org')
router.register(r'register_org_member',views.CreateOrgMemberViewSet ,basename='register_org_member')
urlpatterns = [
    path('',include(router.urls))    
]

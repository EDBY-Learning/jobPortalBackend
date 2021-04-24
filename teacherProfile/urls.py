from django.urls import path, include
from . import views
import os

from rest_framework.routers import DefaultRouter, SimpleRouter

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register(r'register',views.TeacherRegistrationViewset ,basename='register_teacher')
router.register(r'education',views.TeacherEducationViewset ,basename='education_teacher')
router.register(r'qualification',views.TeacherQualificationViewset,basename='qualification_teacher')
router.register(r'experience',views.TeacherExperienceViewset,basename='education_teacher')
router.register(r'language',views.TeacherLanguageViewset,basename='language_teacher')

urlpatterns = [
    path('',include(router.urls)),
    path("lookingfor/subject/",views.TeacherLookingForSubjects.as_view()),
    path("lookingfor/posiiton/",views.TeacherLookingForPositions.as_view()),
    path("lookingfor/country/",views.TeacherLookingForCountry.as_view())
]
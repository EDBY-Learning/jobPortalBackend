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
router.register(r'preference',views.TeacherPreferenceViewset,basename='preference_teacher')
router.register(r'profile',views.TeacherProfileViewset,basename="profile_teacher")
router.register(r'public_profile',views.TeacherPublicProfileViewset,basename="public_profile_teacher")
router.register(r'teachers_applied_for_job',views.FetchTeacherAppliedForJob,basename="teachers_applied_for_job")
router.register(r'basic_profile',views.TeacherBasicProfileViewset,basename="basic_profile")

urlpatterns = [
    path('',include(router.urls)),
    path("bookmark/",views.BookmarkJobViewset.as_view()),
    path("bookmark/<int:pk>/",views.BookmarkJobViewset.as_view()),
    path("apply_for_job/",views.ApplyForAdminJobViewset.as_view()),
    path("get_teacher_list/",views.TeacherList.as_view()),
    path("get_mail_data/",views.MailDataView.as_view())
    #path('profile/<int:pk>/',views.TeacherProfile.as_view(), name='teacher_profile'),
    
]

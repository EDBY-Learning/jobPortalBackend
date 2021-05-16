from django.urls import path, include
from . import views 
import os 

from rest_framework.routers import DefaultRouter, SimpleRouter

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'add_chapter',views.BoardClassChapterViewset ,basename='add_chapter')
router.register(r'get_chapter_topic',views.GetChapterTopicViewset ,basename='get_chapter_topic')
router.register(r'add_chapter_topic',views.ChapterTopicViewset ,basename='add_chapter_topic')
router.register(r'add_chapter_prerequisite',views.ChapterPrerequisiteViewset ,basename='add_chapter_prerequisite')
router.register(r'add_question',views.AdaptiveQuestionViewset ,basename='add_question')
# router.register(r'add_topic_and_prerequisite_question',views.QuestionTopicsPrerequisiteViewset ,basename='add_topic_and_prerequisite_question')

urlpatterns = [
    path('',include(router.urls)),
    # path('search/',views.JobSearchResult.as_view())
]
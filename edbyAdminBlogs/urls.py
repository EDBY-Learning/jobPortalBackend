from django.urls import path, include
from . import views
import os

from rest_framework.routers import DefaultRouter, SimpleRouter

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register(r'add_job_blog',views.JobBlogsViewset ,basename='add_job_blog')
router.register(r'add_job_blog_like',views.JobBlogsLikeDislikeViewset ,basename='add_job_blog_like')
router.register(r'add_job_blog_comment',views.JobBlogsCommentViewset ,basename='add_job_blog_comment')
router.register(r'view_job_blog_detail',views.FetchBlogDetailViewset ,basename='view_job_blog_detail')
router.register(r'blog_comments',views.FetchBlogCommentsViewset ,basename='blog_comments')

urlpatterns = [
    path('',include(router.urls)),
    path('all_blogs/',views.JobBlogsList.as_view()),
    path('like_blog/',views.JobBlogLike.as_view())
    # path("temp/",views.),
    
]

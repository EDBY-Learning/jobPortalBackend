from django.shortcuts import render
from . import serializers as mySerializers
from .models import (
    JobBlogs,
    JobBlogsLikeDislike,
    JobBlogsComment
) 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly 
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.views import APIView
from permissions import manage_permissions as perm 
from utils.operations import update_with_partial


class JobBlogsViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    permission_classes_by_action = {'create': [IsAuthenticated & IsAdminUser],
                                    'list': [IsAuthenticated & IsAdminUser],
                                    'retrieve':[AllowAny],
                                    'update': [IsAuthenticated & IsAdminUser],
                                    'partial_update':[IsAuthenticated & IsAdminUser],
                                    'destroy':[IsAuthenticated & IsAdminUser]}
    queryset = JobBlogs.objects.all().order_by("-entry_time")
    serializer_class = mySerializers.JobBlogsSerializer

    def get_permissions(self):
        return perm.get_custom_permissions(self)

    def update(self, request,  *args, **kwargs):
       return update_with_partial(self, request,  *args, **kwargs)

    #call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
       kwargs['partial'] = True
       return self.update(request, *args, **kwargs)

class JobBlogsLikeDislikeViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = JobBlogsLikeDislike.objects.all().order_by("-entry_time")
    serializer_class = mySerializers.JobBlogsLikeDislikeSerializer


class JobBlogsCommentViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'destroy':[IsAuthenticated & IsAdminUser]
    }
    queryset = JobBlogsComment.objects.all().order_by("-entry_time")
    serializer_class = mySerializers.JobBlogsCommentSerializer

    def get_permissions(self):
        return perm.get_custom_permissions(self)

class FetchBlogDetailViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = mySerializers.FetchBlogDetailSerializer
    queryset = JobBlogs.objects.all().order_by("-entry_time")

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        instance = self.get_object()
        if request.user.is_authenticated:
            try:
                userLike = JobBlogsLikeDislike.objects.filter(blog=instance,user=request.user).first()
            except Exception as e:
                userLike = None
        else:
            userLike = None
        serializer = self.get_serializer({
            "blog":instance,
            "likes":JobBlogsLikeDislike.objects.filter(blog=instance,like=True).count(),
            "dislikes":JobBlogsLikeDislike.objects.filter(blog=instance,like=False).count() ,
            "comment":JobBlogsComment.objects.filter(blog=instance).order_by("-entry_time")[:50],
            "userLike": userLike
        })
        return Response(serializer.data,status=200)

class JobBlogsList(APIView):
    permission_classes = [AllowAny]

    def get(self,request,format=None):
        if request.user.is_authenticated:
            likes = JobBlogsLikeDislike.objects.filter(user=request.user).all().order_by("-entry_time")[:300]
            num_posts = 200
        else:
            likes = []
            num_posts = 20

        blogs = JobBlogs.objects.all().order_by("-entry_time")[:20]
        all_blogs = [blog.to_dict() for blog in blogs]
        # likes = JobBlogsLikeDislike.objects.filter(user=request.user).all().order_by("-entry_time")[:300]
        all_likes = [like.to_dict() for like in likes]
        return Response({'blogs':all_blogs,'likes':all_likes},status=status.HTTP_200_OK)

class JobBlogLike(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        blogId = request.data.get('blogId',None)
        if not blogId:
            return Response('Provide blog id',status=status.HTTP_406_NOT_ACCEPTABLE)
        user_like = int(request.data.get('like',1))
        blog = JobBlogs.objects.get(id=blogId)
        like_saved = JobBlogsLikeDislike.objects.update_or_create(user=request.user,blog=blog,defaults={"like":bool(user_like)})
        # total_like = JobBlogsLikeDislike.objects.filter(blog=blog,like=True).count()
        total_like  = blog.total_like + 1
        blog.total_like = total_like 
        blog.save()
        return Response({'data':user_like,'total_like':total_like},status=status.HTTP_200_OK)

class FetchBlogCommentsViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = mySerializers.FetchBlogCommentsSerializer
    queryset = JobBlogs.objects.all().order_by("-entry_time")

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        instance = self.get_object()
        serializer = self.get_serializer({
           "comment":JobBlogsComment.objects.filter(blog=instance).order_by("-entry_time")[:50]
        })
        return Response(serializer.data,status=200)
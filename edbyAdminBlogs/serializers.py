from teacherProfile.serializers import UserSerializer
from .models import (
    JobBlogs,
    JobBlogsLikeDislike,
    JobBlogsComment
) 

from rest_framework import serializers

class JobBlogsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = JobBlogs
        fields = ("id","title","body","link","user","tags","total_like","entry_time")
        read_only_fields = ('id',"total_like","entry_time","user")
        extra_kwargs = {
            'title':{'required':True},
            'body':{'required':True}
        }

    def create(self, validated_data):
        request = self.context.get('request',None)
        #print(request.user)
        blog = JobBlogs.objects.create(user=request.user,**validated_data)
        return blog


class JobBlogsLikeDislikeSerializer(serializers.ModelSerializer):
    blog = JobBlogsSerializer(read_only=True)
    blogId = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = JobBlogsLikeDislike
        fields = ('id','blog',"blogId","like")
    
    def create(self, validated_data):
        blog = JobBlogs.objects.get(id=validated_data.pop("blogId"))
        request = self.context.get('request',None)
        likeDislike = JobBlogsLikeDislike.objects.create(blog=blog,user=request.user,**validated_data)
        return likeDislike

class JobBlogsCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    blogId = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = JobBlogsComment
        fields = ('id',"blogId","user","comment","total_like","entry_time")
        read_only_fields = ('id',"total_like","entry_time")
        extra_kwargs = {
            'comment':{'required':True}
        }

    def create(self, validated_data):
        blog = JobBlogs.objects.get(id=validated_data.pop("blogId"))
        request = self.context.get('request',None)
        comment = JobBlogsComment.objects.create(blog=blog,user=request.user,**validated_data)
        # total_comment = JobBlogsComment.objects.filter(blog=blog,like=True).count()
        total_comment = blog.total_comment +1
        blog.total_comment =  total_comment
        blog.save()
        return comment

class FetchBlogDetailSerializer(serializers.Serializer):
    blog = JobBlogsSerializer(read_only=True)
    likes = serializers.CharField(read_only=True)
    dislikes = serializers.CharField(read_only=True)
    comment = JobBlogsCommentSerializer(read_only=True,many=True)
    userLike = JobBlogsLikeDislikeSerializer(read_only=True)

    class Meta:
        fields = ("blog","likes","dislikes","comment","userLike")
        exclude = ('id',)

class FetchBlogCommentsSerializer(serializers.Serializer):
    comment = JobBlogsCommentSerializer(read_only=True,many=True)
    
    class Meta:
        fields = ("comment",)
        exclude = ('id',)

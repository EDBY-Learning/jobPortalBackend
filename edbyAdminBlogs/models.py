from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobBlogs(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = models.CharField(max_length=300)
    link = models.CharField(max_length=300,blank=True,null=True)
    total_like = models.IntegerField(default=0,blank=True,null=True)
    total_comment = models.IntegerField(default=0,blank=True,null=True)
    entry_time = models.DateTimeField(auto_now=False,auto_now_add=True)
    
    def to_dict(self):
        info_dict = {}
        for key in ["id",'title','body','link','tags','total_like','total_comment','entry_time']:
            info_dict[key] = self.__dict__[key].__str__()
        info_dict['user'] = {'first_name':self.user.first_name}
        return info_dict


class JobBlogsLikeDislike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(JobBlogs,on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    entry_time = models.DateTimeField(auto_now=True,auto_now_add=False)

    def to_dict(self):
        info_dict = {}
        for key in ['like','entry_time']:
            info_dict[key] = self.__dict__[key].__str__()
        info_dict['blogId'] = self.blog.id
        return info_dict

class JobBlogsComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(JobBlogs,on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    entry_time = models.DateTimeField(auto_now=True,auto_now_add=False)
    total_like = models.IntegerField(default=0,blank=True,null=True)
    def to_dict(self):
        info_dict = {}
        for key in ['comment','total_like','entry_time']:
            info_dict[key] = self.__dict__[key].__str__()
        info_dict['blogId'] = self.blog.id
        return info_dict

class JobBlogsCommentLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(JobBlogsComment,on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    entry_time = models.DateTimeField(auto_now=True,auto_now_add=False)

    def to_dict(self):
        info_dict = {}
        for key in ['like','entry_time']:
            info_dict[key] = self.__dict__[key].__str__()
        info_dict['blogId'] = self.comment.id
        return info_dict
    


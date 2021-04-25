from django.db import models
from datetime import date
from django.core.validators import RegexValidator
from django.dispatch import receiver


#PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
from uuid import uuid4
from datetime import datetime, timedelta
import os
def get_unique_full_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(instance.pk)+uuid4().hex,ext)
    # return the whole path to the file
    return os.path.join('images/', filename)

class JobSearch(models.Model):
    city = models.CharField(max_length=200,null=True,blank=True)
    positions = models.CharField(max_length=200,null=True,blank=True)
    subjects = models.CharField(max_length=200,null=True,blank=True)
    usernamefake = models.CharField(max_length=20,null=True,blank=True)
    result_count = models.IntegerField(default=0)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

class UserNextClick(models.Model):
    usernamefake = models.CharField(max_length=20,null=True,blank=True)
    next_page = models.CharField(max_length=20,null=True,blank=True)
    from_page = models.CharField(max_length=20,null=True,blank=True)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

class FeedbackByUser(models.Model):
    usernamefake = models.CharField(max_length=20)
    from_page = models.CharField(max_length=20,null=True,blank=True)
    feedback= models.CharField(max_length=300,null=True,blank=True)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

class JobInfo(models.Model):
    school = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    contact = models.CharField( max_length=17)

    #Keeping as string field comma seperated - "Teacher,Principal"
    positions = models.CharField(max_length=200,null=True,blank=True)

    #Keeping as string field comma seperated - "Maths, Physics"
    subjects = models.CharField(max_length=200,null=True,blank=True)

    url = models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(upload_to=get_unique_full_path, max_length=200, blank=True, null=True)
    #by default edby
    isByEdby = models.BooleanField(default=True)
    message = models.CharField(max_length=100,blank=True,null=True)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def to_dict(self):

        info_dict = {}
        for key in ['school','city','address','email','contact','positions','subjects','url','image','isByEdby',
                    'message','entry_time','id']:
                    info_dict[key] = self.__dict__[key].__str__()
        if self.image:
            info_dict['image_url'] = self.image.url
        return info_dict

@receiver(models.signals.pre_delete, sender=JobInfo)
def remove_file_from_s3(sender, instance, **kwargs):
    instance.image.delete(save=False)



#To remove this file from amazon S3 bucket
class JobPostByOutSider(models.Model):
    school = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)
    contact = models.CharField(max_length=50,null=True,blank=True)

    #Keeping as string field comma seperated - "Teacher,Principal"
    positions = models.CharField(max_length=200,null=True,blank=True)

    #Keeping as string field comma seperated - "Maths, Physics"
    subjects = models.CharField(max_length=200,null=True,blank=True)

    message = models.CharField(max_length=200,blank=True,null=True)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

    is_published = models.BooleanField(default=False)

    def to_dict(self):

        info_dict = {}
        for key in ['school','city','address','email','contact','positions','subjects',
                    'message','entry_time']:
                    info_dict[key] = self.__dict__[key].__str__()
        return info_dict
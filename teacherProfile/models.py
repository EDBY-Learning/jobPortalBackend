from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.signals import user_logged_in

from jobPortal.models import (
    JobInfo,
    AdminJobPost
)

RWST = (
    (1, ("No")),
    (2, ("Basic")),
    (3, ("Intermediate")),
    (4, ("Fluent"))
)

# Create your models here.
class TeacherBasicInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="teacher_user")
    country_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    country = models.CharField(max_length=40)
    dob = models.DateField(blank=True,null=True)
    description = models.CharField(max_length=2000,blank=True,null=True)
    email = models.EmailField(max_length=150)
    login_count = models.PositiveIntegerField(default=0,blank=True,null=True)

    def to_dict(self):
        info_dict = {}
        for key in ['mobile','email','country']:
            info_dict[key] = self.__dict__[key].__str__()
        info_dict['name'] = self.user.first_name
        info_dict['date_joined'] = self.user.date_joined
        return info_dict

# def login_user(sender, request, teacher, **kwargs):
#     teacher.login_count = teacher.login_count + 1
#     teacher.userprofile.save()

# user_logged_in.connect(login_user)

class TeacherEducation(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    score = models.CharField(max_length=20)

class TeacherQualifications(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    major_subject = models.CharField(max_length=100)
    start_date = models.CharField(max_length=4)
    end_date = models.CharField(max_length=4)
    score = models.CharField(max_length=20)

class TeacherExperience(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    institute = models.CharField(max_length=100)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4,blank=True,null=True)
    ongoing = models.BooleanField(default=False)
    #comma separated subjects
    subjects = models.CharField(max_length=200)
    #comma separated classes
    classes = models.CharField(max_length=100)

class TeacherLanguage(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    language = models.CharField(max_length=30)
    can_write = models.IntegerField(choices=RWST,default=3)
    can_read = models.IntegerField(choices=RWST,default=3)
    can_speak = models.IntegerField(choices=RWST,default=3)
    can_teach = models.IntegerField(choices=RWST,default=3)
 
class TeacherPreference(models.Model):
    teacher = models.OneToOneField(TeacherBasicInfo,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

class TeacherBookmarkedJob(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    job = models.ForeignKey(JobInfo,on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

APPLICATION_STATUS=(
    (1,("Applied")),
    (2,("Sent Resume To School")),
    (3,("Selected for Interview")),
    (4,("Application Declined")),
    (5,("Closed, No more application")),
)
class TeacherAppliedAdminJob(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    job = models.ForeignKey(AdminJobPost,on_delete=models.CASCADE)
    status = models.IntegerField(choices=APPLICATION_STATUS,default=1)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)
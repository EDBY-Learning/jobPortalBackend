from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator

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
    start_date = models.DateField()
    end_date = models.DateField()
    score = models.CharField(max_length=20)

class TeacherExperience(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    institute = models.CharField(max_length=100)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    ongoing = models.BooleanField(default=False)
    #comma separated subjects
    sujects = models.CharField(max_length=200)
    #comma separated classes
    classes = models.CharField(max_length=100)

class TeacherLanguage(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    language = models.CharField(max_length=30)
    can_write = models.IntegerField(choices=RWST,default=3)
    can_read = models.IntegerField(choices=RWST,default=3)
    can_speak = models.IntegerField(choices=RWST,default=3)
    can_teach = models.IntegerField(choices=RWST,default=3)
 
class SubjectLookingFor(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    subject = models.CharField(max_length=30)

class PositionLookingFor(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    position = models.CharField(max_length=30)

class CountryLookingFor(models.Model):
    teacher = models.ForeignKey(TeacherBasicInfo,on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
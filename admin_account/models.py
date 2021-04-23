from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
# https://stackoverflow.com/questions/47691718/django-creating-a-custom-user-with-the-django-rest-framework
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

ORG_TYPE = (
    (1, ("Start Up")),
    (2, ("Project")),
    (3, ("Exploring"))
)

# SUB_TYPE = (
#     (1, ("Free")),
#     (2, ("Silver Plan")),
#     (3, ("Gold Plan")),
#     (4, ("Custom Plan"))
# )

# class Subscription(models.Model):
#     sub_type = models.IntegerField(choices=SUB_TYPE, default=1)

class Organization(models.Model):    
    company = models.CharField(max_length=60)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    organization_type = models.IntegerField(choices=ORG_TYPE, default=1)
    #org_field = models.CharField(max_length=60,blank=True,null=True)
    public = models.BooleanField(default=True)

class UserInfo(models.Model):
    mobile = models.CharField(max_length=13)
    country = models.CharField(max_length=60)
    org_email = models.EmailField(max_length=150,blank=True,null=True)
    college = models.CharField(max_length=100,blank=True,null=True)
    work_experience = models.IntegerField(default=1,validators=[MinValueValidator(0)],blank=True,null=True)
    description = models.CharField(max_length=1000,blank=True,null=True)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)

class OrganizationMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="org_user_set")
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE)
    user_info = models.OneToOneField(UserInfo,on_delete=models.CASCADE,related_name="user_info_set")

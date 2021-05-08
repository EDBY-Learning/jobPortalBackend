from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ForgotPasswordData(models.Model):
    email = models.EmailField(max_length=150,blank=True,null=True)
    mobile = models.CharField(max_length=15,blank=True,null=True)
    username = models.CharField(max_length=20,blank=True,null=True)

from django.db import models

# Create your models here.
class ForgotPasswordData(models.Model):
    email = models.EmailField(max_length=150,blank=True,null=True)
    mobile = models.CharField(max_length=15,blank=True,null=True)
    username = models.CharField(max_length=20,blank=True,null=True)
    status = models.BooleanField(default=False)

class ChangedForgotPassword(models.Model):
    username = models.CharField(max_length=20,blank=True,null=True)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)
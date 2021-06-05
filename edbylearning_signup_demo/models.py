from django.db import models

# Create your models here.

class SignUp(models.Model):
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=15,blank=True,null=True)
    name = models.CharField(max_length=40,blank=True,null=True)
    demo = models.BooleanField(default=False)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)


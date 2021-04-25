from django.db import models


class TestModel(models.Model):
    test_text = models.CharField(max_length=200,null=True,blank=True)

class ClickCRM(models.Model):
    username = models.CharField(max_length=20,null=True,blank=True)
    is_logged = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    current_page = models.CharField(max_length=20,null=True,blank=True)
    click_on = models.CharField(max_length=20,null=True,blank=True)
    next_page = models.CharField(max_length=20,null=True,blank=True)
    other_info = models.CharField(max_length=20,null=True,blank=True)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

class SearchCRM(models.Model):
    username = models.CharField(max_length=20,null=True,blank=True)
    is_logged = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    city = models.CharField(max_length=200,null=True,blank=True)
    positions = models.CharField(max_length=200,null=True,blank=True)
    subjects = models.CharField(max_length=200,null=True,blank=True)
    result_count = models.IntegerField(default=0)
    is_forced = models.BooleanField(default=False)
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

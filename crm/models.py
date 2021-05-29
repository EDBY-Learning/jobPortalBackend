from fcm_django.models import AbstractFCMDevice
from teacherProfile.models import TeacherBasicInfo
from django.db import models


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

class CustomFCMDevice(AbstractFCMDevice):
    DEVICE_TYPES = (
        (u'ios', u'ios'),
        (u'android', u'android'),
        (u'web', u'web'),
        (u'pc',u'pc')
    )
    type = models.CharField(choices=DEVICE_TYPES, max_length=10)

    class Meta:
        verbose_name = 'Custom FCM device'
        verbose_name_plural = 'Custom FCM devices'

PassKeyMember = (
    ("all",('All')),
    ("registered",('Registered Teachers')),
    ("unregistered",('Unregistered Teachers'))
)

class PassKeyNotifications(models.Model):
    whom = models.CharField(primary_key=True ,max_length=100, choices=PassKeyMember)
    passkey = models.CharField(max_length=10)

class FCMClickRate(models.Model):
    query_param = models.CharField(max_length=100)
    whom = models.CharField(max_length=100,choices=PassKeyMember)
    notification_sent = models.IntegerField()
    notification_opened = models.IntegerField(null=True,blank=True)

FCM_ACTION = (
    (1,('Other')),
    (2,('Register')),
    (3,('Logged In')),
    (4,('Built Resume')),
    (5,('Opened Blog')),
    (6,('Applied For Admin Job'))
)

class FCMUserAction(models.Model):
    fcm_query_key = models.ForeignKey(FCMClickRate,on_delete=models.CASCADE)
    action = models.IntegerField(choices=FCM_ACTION,default=1)

class TeacherNotifications(models.Model):
    teacher = models.OneToOneField(TeacherBasicInfo,on_delete=models.CASCADE)
    resume_complete = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True,auto_now_add=False)

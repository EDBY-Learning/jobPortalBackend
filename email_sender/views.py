from django.shortcuts import render
from django.http import HttpResponse
from .models import MailRequest
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

def createWelcomeMail(email):
    message = """
    Hey, 
    Welcome to our site, this is confirmation mail please don't reply as you won't get response!!!
    """
    mailrequest = MailRequest.objects.create(message=message,email=email)
    mailrequest.save()

def createResetMail(email,token):
    message = """
    Hey, 
    This is Reset mail please don't reply as you won't get response!!!
    Token: 
    """ +token
    mailrequest = MailRequest.objects.create(message=message,email=email,mail_type=2)
    mailrequest.save()

class SendEmail(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        mails = MailRequest.objects.filter(mail_type=1,status=1)
        for mail in mails:
            print(mail)

        return HttpResponse("success")


        
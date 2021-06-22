from django.shortcuts import render
from django.http import HttpResponse
from .models import MailRequest
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from .utils.sheet.append import append_values
from .utils.sheet.populate import populate_values
from .services import gmail, gsheet

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

SCOPES = ['https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/gmail.send']

def setup():
    creds = None
    if os.path.exists(str(BASE_DIR)+"/"+'token.json'):
        creds = Credentials.from_authorized_user_file(str(BASE_DIR)+"/"+'token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Refreshing Token!!')
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(BASE_DIR)+"/"+'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(str(BASE_DIR)+"/"+'token.json', 'w') as token:
            token.write(creds.to_json())
    print("got credentials")
    return creds

creds = setup()
sheet_service = gsheet.getSheetHandle(creds)
spreadsheet_id = "1GTLCHCASpjSSgvgx2RqNA268mlsuRdkb8bSAINr8a0A"
mail_service = gmail.getMailHandle(creds)

def refreshHandle():
    global creds, sheet_service, mail_service
    creds = setup()
    sheet_service = gsheet.getSheetHandle(creds)
    mail_service = gmail.getMailHandle(creds)


def createWelcomeMail(email):
    message = """
    Hey, \n
    Welcome to our site, this is confirmation mail please don't reply as you won't get response!!! \n
    Regards,\n
    EDBY Team \n
    """
    mailrequest = MailRequest.objects.create(message=message,email=email)
    mailrequest.save()

def createResetMail(username,email,token):
    body = f"""
    Hey, \n
    Mobile/Username: {username} \n
    This is Reset mail please don't reply as you won't get a response!!! \n
    Token: {token}\n\n
    Go here: https://jobportal.edbylearning.com/dashboard/pages/examples/publicchangepassword.html?token={token} \n

    And use this token to reset email. It is valid till next 48 hours. \n
    Sorry if any delay\n\n
    Regards,\n
    EDBY Team \n
    """ 
    mailrequest = MailRequest.objects.create(message=body,email=email,mail_type=2)
    mailrequest.save()
    if creds and creds.expired and creds.refresh_token:
        refreshHandle()
    try:
        message = gmail.create_message(email,"Forgot Password Reset",body)
        gmail.SendMessageInternal(mail_service,'me',message)
    except Exception as e:
        print(str(e))

class SendEmail(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        mails = MailRequest.objects.filter(mail_type=1,status=1)
        for mail in mails:
            print(mail)

        return HttpResponse("success")


        
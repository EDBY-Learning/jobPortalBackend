from googleapiclient.discovery import build
from pathlib import Path
from email.mime.text import MIMEText
from apiclient import errors, discovery
import base64


BASE_DIR = Path(__file__).resolve().parent
DELIMITER = "<:>"
FROM = "edbytechteam@gmail.com"

def getMailHandle(creds):
    return build('gmail', 'v1', credentials=creds)

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        # print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"

def create_message( to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = FROM
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
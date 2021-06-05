from email_sender.models import MailRequest

def send_forgot_password_mail(email):
    mail = MailRequest.objects.filter(email=email).first()
    if mail:
        if not mail.email:
            return False
        elif mail.email=='':
            return False 
        elif mail.email=='-':
            return False 
        return True
    else:
        return False
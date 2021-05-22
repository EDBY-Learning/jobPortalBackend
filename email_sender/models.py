from django.db import models

MAIL_STATUS = (
    (1, ("Not Sent")),
    (2, ("Sent"))
)

MAIL_TYPE = (
    (1, ("New Registration")),
    (2, ("Password Reset")),
    (3, ("Other"))
)

class MailRequest(models.Model):
    message = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    mail_type = models.IntegerField(choices=MAIL_TYPE, default=1)
    status = models.IntegerField(choices=MAIL_STATUS, default=1)   
    entry_time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def to_dict(self):
        info_dict = {}
        for key in ['email','mail_type','status','message','entry_time']:
            info_dict[key] = self.__dict__[key].__str__()
        return info_dict
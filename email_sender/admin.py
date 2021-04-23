from django.contrib import admin
from .models import MailRequest
# Register your models here.

class MailRequestAdmin(admin.ModelAdmin):
    list_filter = ('email','status','mail_type')
    list_display = ["email","mail_type","status","message","entry_time"]

admin.site.register(MailRequest, MailRequestAdmin)
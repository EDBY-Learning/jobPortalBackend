from django.contrib import admin
from .models import ForgotPasswordData
from utils.mail_system import send_forgot_password_mail


@admin.register(ForgotPasswordData)
class ForgotPasswordDataView(admin.ModelAdmin):
    list_display = ("mobile","email","username","status","mail_status","failure")
    search_fields = ("mobile","email")
    list_filter = ("status","mail_status","failure")
    actions = ["mark_true","mark_false","mail_user","unmail_user","remove_failure"]

    def mark_true(self, request, queryset):
        queryset.update(status=True,mail_status=2)
    
    def mark_false(self, request, queryset):
        queryset.update(status=False)

    def mail_user(self, request, queryset):
        for query in queryset:
            trigger = send_forgot_password_mail(query.email)
            if trigger:
                query.mail_status=2
                query.save()
            else:
                query.failure=True
                query.save()
    
    def unmail_user(self, request, queryset):
        queryset.update(mail_status=1)
    
    def remove_failure(self, request, queryset):
        queryset.update(failure=False)

    mark_true.short_description = "Status True"
    mark_false.short_description = "Status False"
    mail_user.short_description = "Send Mail"
    unmail_user.short_description = "Not Sent"
    remove_failure.short_description = "Passed"



from django.contrib import admin
from .models import ForgotPasswordData, ChangedForgotPassword

# Register your models here.
@admin.register(ForgotPasswordData)
class ForgotPasswordDataView(admin.ModelAdmin):
    list_display = ("mobile","email","username","status")
    search_fields = ("mobile","email")
    list_filter = ("status",)

@admin.register(ChangedForgotPassword)
class ChangedForgotPasswordView(admin.ModelAdmin):
    list_display = ("username","entry_time")
    search_fields = ("username",)

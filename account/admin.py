from django.contrib import admin
from .models import ForgotPasswordData

# Register your models here.
@admin.register(ForgotPasswordData)
class TeacherInfoView(admin.ModelAdmin):
    list_display = ("mobile","email","username")
    search_fields = ("mobile","email")
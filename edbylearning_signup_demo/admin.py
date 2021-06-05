from django.contrib import admin
from .models import SignUp
# Register your models here.
@admin.register(SignUp)
class SignUpView(admin.ModelAdmin):
    list_display = ("email","mobile","name","demo","entry_time")
    list_filter  = ("demo",)
    # search_fields = ("city","positions","subjects")
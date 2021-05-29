from django.contrib import admin
from .models import (CustomFCMDevice, FCMUserAction, FCMClickRate, PassKeyNotifications, TeacherNotifications,
                ClickCRM,SearchCRM)


@admin.register(ClickCRM)
class ClickCRMView(admin.ModelAdmin):
    list_display = ("username","current_page","entry_time")
    list_filter  = ("username","current_page")


@admin.register(SearchCRM)
class SearchCRMView(admin.ModelAdmin):
    list_display = ("city","positions","subjects","result_count","username","entry_time")
    # list_filter  = ("subjects","positions")
    search_fields = ("city","positions","subjects")

class FCMUserActionInline(admin.TabularInline):
    model = FCMUserAction

@admin.register(FCMClickRate)
class FCMClickRateView(admin.ModelAdmin):
    list_display = ("query_param","notification_sent","notification_opened")

    inlines = [FCMUserActionInline]

@admin.register(TeacherNotifications)
class TeacherNotificationView(admin.ModelAdmin):
    list_display = ("teacher","resume_complete",'last_seen')

@admin.register(CustomFCMDevice)
class CustomFCMDeviceView(admin.ModelAdmin):
    list_display = ("user","name", "registration_id", "device_id", "active",
            "date_created", "type")
    list_filter = ("name","active","type")
    search_fields = ("registration_id","type")

@admin.register(PassKeyNotifications)
class PassKeyNotificationsAdminView(admin.ModelAdmin):
    list_display = ('whom','passkey')
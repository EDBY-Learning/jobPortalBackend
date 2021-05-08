from django.contrib import admin
from .models import (TestModel,
                ClickCRM,SearchCRM)



@admin.register(TestModel)
class TestModelView(admin.ModelAdmin):
    list_display = ("test_text",)

@admin.register(ClickCRM)
class ClickCRMView(admin.ModelAdmin):
    list_display = ("username","current_page","entry_time")
    list_filter  = ("username","current_page")


@admin.register(SearchCRM)
class SearchCRMView(admin.ModelAdmin):
    list_display = ("username","result_count","entry_time")
    list_filter  = ("username","subjects")

from skillDevelopment.models import EdbyFreeCourseContent, PartnerCourses, PartnerDetail
from django.contrib import admin

# Register your models here.
class FreeCourseContent(admin.TabularInline):
    model = EdbyFreeCourseContent
    fields = ("num","link","description")

@admin.register(PartnerCourses)
class PartnerCoursesView(admin.ModelAdmin):
    list_display = ('title',"course_link","group_name","group_link","total_like","isByEdby","active","entry_time")
    search_fields = ('title',"course_link","group_name")
    actions = ['mark_active','mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(active=True)
    
    def mark_inactive(self, request, queryset):
        queryset.update(active=False)

    inlines = [FreeCourseContent]

@admin.register(PartnerDetail)
class PartnerList(admin.ModelAdmin):
    list_display = ('name','whatsapp_group')
    search_fields = ('name',)

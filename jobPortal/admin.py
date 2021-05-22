from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import AdminJobPost, JobInfo, JobPostByOutSider,FeedbackByUser

def publish_job(modeladmin, request, queryset):
    batch_size = 100
    data_list = [job.to_dict() for job in queryset.all()]
    object_list = [AdminJobPost(**{**data,'isByEdby':False}) for data in data_list]
    objs = AdminJobPost.objects.bulk_create(object_list,batch_size)

    #should we delete or just update is_published
    queryset.update(is_published=True)
    # queryset.delete()


class FeedbackByUserAdmin(admin.ModelAdmin):
    search_fields = ('usernamefake','from_page','feedback')
    list_display =  ('usernamefake','from_page','feedback','entry_time')
    ordering = ['entry_time']

class JobInfoAdmin(admin.ModelAdmin):
    #list_filter = ('school','city','positions','subjects','url','entry_time',)
    list_display = ['school','city','positions','subjects','email','contact','url','image']
    search_fields = ('positions', 'school', 'subjects','city' )
    list_per_page = 50

    ordering = ['entry_time']
    #readonly_fields = ["image_view",]

    def image_view(self, obj):
        if obj.image:
            url = obj.image.url
        else:
            url = ''
        return mark_safe('<img src="{url}" width="{width}" height={height} onerror="this.style.opacity=0"/>'.format(
            url = url,
            width=200,
            height=200,
            )
    )
class JobPostByOutSiderAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in JobPostByOutSider._meta.get_fields() if (not field.many_to_many) and (not field.one_to_many)]
    list_display = ["is_published",'school','city','positions','subjects','email','contact','message','entry_time']
    odering = ['entry_time']
    actions = [publish_job]

class AdminJobPostAdmin(admin.ModelAdmin):
    list_display = ["school","city","email","contact",'message',"image"]
    search_fields = ("school","city","email","contact")

admin.site.register(JobPostByOutSider,JobPostByOutSiderAdmin)
admin.site.register(JobInfo, JobInfoAdmin)
admin.site.register(FeedbackByUser, FeedbackByUserAdmin)
admin.site.register(AdminJobPost,AdminJobPostAdmin)
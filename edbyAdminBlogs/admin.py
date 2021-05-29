from .models import JobBlogs, JobBlogsComment, JobBlogsCommentLike, JobBlogsLikeDislike
from django.contrib import admin

# Register your models here.
class JobBlogCommentInline(admin.TabularInline):
    model = JobBlogsComment
    fields = ("user","comment","total_like")

class JobBlogsLikeDislikeInline(admin.TabularInline):
    model = JobBlogsLikeDislike
    fields = ('user','like')

@admin.register(JobBlogs)
class JobBlogAdminView(admin.ModelAdmin):
    list_display = ('title','total_like','link','tags','entry_time')
    search_fields = ("title","link",'tags')

    inlines = [JobBlogCommentInline,JobBlogsLikeDislikeInline]

class JobBlogsCommentLikeInline(admin.TabularInline):
    model = JobBlogsCommentLike
    fields = ('user','like')

@admin.register(JobBlogsComment)
class JobBlogsCommentAdminView(admin.ModelAdmin):
    list_display = ('user','comment','total_like','entry_time')
    search_fields = ("comment",)

    inlines = [JobBlogsCommentLikeInline]

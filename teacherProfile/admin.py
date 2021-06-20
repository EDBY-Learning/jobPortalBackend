from django.contrib import admin
from .models import (
    TeacherAppliedAdminJob,
    TeacherBasicInfo,
    TeacherEducation,
    TeacherExperience,
    TeacherLanguage,
    TeacherQualifications,
    TeacherPreference,
    TeacherBookmarkedJob)
# Register your models here.

class TeacherEducationInline(admin.TabularInline):
    model = TeacherEducation

class TeacherExperienceInline(admin.TabularInline):
    model = TeacherExperience

class TeacherQualificationsInline(admin.TabularInline):
    model = TeacherQualifications

class TeacherLanguageInline(admin.TabularInline):
    model = TeacherLanguage

class TeacherPreferenceInline(admin.TabularInline):
    model = TeacherPreference


@admin.register(TeacherBasicInfo)
class TeacherInfoView(admin.ModelAdmin):
    list_display = ("mobile","email","country")
    list_filter = ("country",)
    search_fields = ("mobile","email","country","description")

    inlines = [
        TeacherEducationInline,
        TeacherExperienceInline,
        TeacherQualificationsInline,
        TeacherLanguageInline,
        TeacherPreferenceInline]

@admin.register(TeacherBookmarkedJob)
class TeacherBookmarkedJobView(admin.ModelAdmin):
    list_display = ("teacher_name","job_id")

    def teacher_name(self,x):
        return x.teacher.user.first_name

    def job_id(self,x):
        return x.job.id
    
@admin.register(TeacherPreference)
class TeacherPreferenceList(admin.ModelAdmin):
    list_display = ("teacher","subject","position","location","country")

@admin.register(TeacherAppliedAdminJob)
class TeacherAppliedAdminJobView(admin.ModelAdmin):
    list_display = ("teacher_name","job_id","status")

    def teacher_name(self,x):
        return x.teacher.user.first_name

    def job_id(self,x):
        return x.job.id













from django.contrib import admin
from .models import (
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
    search_fields = ("country","description")

    inlines = [
        TeacherEducationInline,
        TeacherExperienceInline,
        TeacherQualificationsInline,
        TeacherLanguageInline,
        TeacherPreferenceInline]

@admin.register(TeacherBookmarkedJob)
class TeacherBookmarkedJobView(admin.ModelAdmin):
    list_display = ("teacher","job")
    
@admin.register(TeacherPreference)
class TeacherPreferenceList(admin.ModelAdmin):
    list_display = ("teacher","subject","position","location","country")














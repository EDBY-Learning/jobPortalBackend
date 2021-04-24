from django.contrib import admin
from .models import (
    TeacherBasicInfo,
    TeacherEducation,
    TeacherExperience,
    TeacherLanguage,
    TeacherQualifications,
    SubjectLookingFor,
    PositionLookingFor,
    CountryLookingFor)
# Register your models here.

class TeacherEducationInline(admin.TabularInline):
    model = TeacherEducation

class TeacherExperienceInline(admin.TabularInline):
    model = TeacherExperience

class TeacherQualificationsInline(admin.TabularInline):
    model = TeacherQualifications

class TeacherLanguageInline(admin.TabularInline):
    model = TeacherLanguage

class SubjectLookingForInline(admin.TabularInline):
    model = SubjectLookingFor

class PositionLookingForInline(admin.TabularInline):
    model = PositionLookingFor

class CountryLookingForInline(admin.TabularInline):
    model = CountryLookingFor

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
        SubjectLookingForInline,
        PositionLookingForInline,
        CountryLookingForInline]



















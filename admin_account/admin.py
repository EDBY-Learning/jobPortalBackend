from .models import Organization, OrganizationMember, UserInfo
from django.contrib import admin

class OrgMemberInline(admin.TabularInline):
    model = OrganizationMember

@admin.register(Organization)
class OrganizationView(admin.ModelAdmin):
    list_display = ("company","organization_type")
    list_filter  = ("organization_type",)
    inlines = [OrgMemberInline]

@admin.register(OrganizationMember)
class OrganizationMemberView(admin.ModelAdmin):
    list_display = ('get_username', 'get_organization','is_admin','is_employee')
    def get_organization(self, x):
        return x.organization.company
    def get_username(self,x):
        return x.user.username
    get_organization.short_description = 'Organization'
    get_username.short_description = 'Username'
    def is_admin(self, x):
        return x.user_info.is_admin
    def is_employee(self,x):
        return x.user_info.is_employee
    is_admin.short_description = 'Is Admin'
    is_employee.short_description = 'Is Employee'

@admin.register(UserInfo)
class UserInfoView(admin.ModelAdmin):
    list_display = ('org_email','college','country','is_admin','is_employee')

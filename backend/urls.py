from django.contrib import admin
from django.urls import path, include
import os
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_4uck/', admin.site.urls),
    path('auth/',include('account.urls')),
    path('teacher/',include('teacherProfile.urls')),
    path('mailer/',include('email_sender.urls')),
    path('details/',include('basicDetails.urls')),
    path('job/',include('jobPortal.urls')),
    path("crm/",include("crm.urls")),
    path('job/v2/',include('jobSearch.urls')),
    path('edby/app/',include('edbyAdaptiveApp.urls')),
    path('edby/blogs/',include('edbyAdminBlogs.urls')),
    path('edbylearning/',include('edbylearning_signup_demo.urls')),
    path('skill_development/',include('skillDevelopment.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# testing_pattern = [
#     path('api-auth/', include('rest_framework.urls')),
#     #path('accounts/', include('django.contrib.auth.urls')),
# ]

# if os.environ.get('ENV')=='local': #and bool(int(os.environ.get("DEBUG",0)))==True:
#     testing_pattern.extend(urlpatterns)
#     urlpatterns = testing_pattern
from crm.models import SearchCRM
def setup():
    SearchCRM.objects.all().delete()
y = 'no'
if y=='yes':
    setup()

from django.contrib import admin
from django.urls import path, include
import os
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_4uck/', admin.site.urls),
    path('auth/',include('account.urls')),
    # path('management/',include('admin_account.urls')),
    path('mailer/',include('email_sender.urls')),
    path('details/',include('basicDetails.urls')),
    path('job/',include('jobPortal.urls')),
    path("crm/",include("crm.urls")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# testing_pattern = [
#     path('api-auth/', include('rest_framework.urls')),
#     #path('accounts/', include('django.contrib.auth.urls')),
# ]

# if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
#     testing_pattern.extend(urlpatterns)
#     urlpatterns = testing_pattern



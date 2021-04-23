"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('ENV') == 'local':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
elif os.environ.get('ENV') == 'dev'  or os.environ.get('ENV')==None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
elif os.environ.get('ENV') == 'deploy':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.deploy')
else:
    raise Exception("ENV variable not stored, please set ENV as local, dev or deploy")
application = get_wsgi_application()

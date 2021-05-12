from pathlib import Path
import os
from datetime import timedelta
import json 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

ENV = "dev"
try:
    with open(str(BASE_DIR)+"/settings/configuration/"+ENV+".json",'r') as f:
        env_var = json.load(f)
except:
    print(("Devlopment configuration file not present at ",str(BASE_DIR)+"/settings/configuration/"+ENV+".json"))
    raise Exception("Devlopment configuration file not present at ",str(BASE_DIR)+"/settings/configuration/"+ENV+".json")

SECRET_KEY = env_var['Basic']['SECRET_KEY']
DEBUG = bool(int(os.environ.get('DEBUG',0)))
ALLOWED_HOSTS = env_var['Basic']["ALLOWED_HOSTS"]

CORS_ALLOWED_ORIGINS =["https://ppritish5153.pythonanywhere.com/"]

#security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True

#When this policy is set, browsers will refuse to connect to your site for the given time period if you’re not properly serving HTTPS resources, or if your certificate expires.
SECURE_HSTS_SECONDS = 86400  # 1 day
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'account',
    'email_sender',
    'basicDetails',
    'teacherProfile',
    'jobPortal',
    'crm',
    "jobSearch"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        "ENGINE": env_var['Database']['ENGINE'],
        "NAME": env_var['Database']['NAME'],
        "USER": env_var['Database']['USER'],
        "PASSWORD": env_var['Database']['PASSWORD'],
        "HOST": env_var['Database']['HOST'],
        "PORT": env_var['Database']['PORT']
    }
}

if DEBUG:
    DEFAULT_RENDERER_CLASSES = ('rest_framework.renderers.BrowsableAPIRenderer',)
else:
    DEFAULT_RENDERER_CLASSES = ( )

REST_FRAMEWORK= {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        
    ),
    "DEFAULT_RENDERER_CLASSES":DEFAULT_RENDERER_CLASSES,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = env_var['Static']['STATIC_URL']
# MEDIA_ROOT = env_var['Static']['MEDIA_ROOT']
# MEDIA_URL = env_var['Static']['MEDIA_URL']
# STATIC_ROOT = env_var['Static']['STATIC_ROOT']

#python anywhere
STATIC_URL = '/static/'
MEDIA_URL = '/home/ppritish5153/base_backend/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/ppritish5153/base_backend/static'

#AWS storages
AWS_ACCESS_KEY_ID = 'AKIAYILN2NTZSFYUVN6Y' #os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = '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' #os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'jobinfo' #os.environ.get('S3_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_EXPIRE = 3600
# DEFAULT_FILE_STORAGE = 'jobPortal.storage_backends.PublicMediaStorage'
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7,minutes=600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'new_siging_key',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer','JWT'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=300),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

EMAIL_USE_TLS = env_var['Email']['EMAIL_USE_TLS']
EMAIL_USE_SSL = env_var['Email']['EMAIL_USE_SSL']
EMAIL_BACKEND = env_var['Email']['EMAIL_BACKEND']
EMAIL_HOST = env_var['Email']['EMAIL_HOST']
EMAIL_HOST_PASSWORD = env_var['Email']['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = env_var['Email']['EMAIL_HOST_USER']
EMAIL_PORT = env_var['Email']['EMAIL_PORT']
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(BASE_DIR)+'/logs/'+ENV+'/debug.log',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(BASE_DIR)+'/logs/'+ENV+'/error.log',
        },
    },
    'loggers': {
        'debug': {
            'handlers': ['debug','error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'error': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
"""
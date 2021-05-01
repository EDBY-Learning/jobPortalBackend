from pathlib import Path
import os
from datetime import timedelta
import json 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

#print("base Dorectory ",BASE_DIR,'Current working Directory ',os.getcwd())
ENV = "local" 
try:
    with open(str(BASE_DIR)+"/settings/configuration/"+ENV+".json",'r') as f:
        env_var = json.load(f)
except:
    raise Exception("local configuration file not present")

SECRET_KEY = env_var['Basic']["SECRET_KEY"]
DEBUG = bool(int(env_var['Basic']['DEBUG']))
ALLOWED_HOSTS = env_var['Basic']["ALLOWED_HOSTS"]

os.environ['DEBUG'] = '1'
CORS_ALLOWED_ORIGINS =["http://localhost:3000","http://localhost:3001"]

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
    'teacherProfile'
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
        "NAME": os.path.join(BASE_DIR, env_var['Database']['NAME'])
    }
}

if DEBUG:
    DEFAULT_RENDERER_CLASSES = ('rest_framework.renderers.JSONRenderer','rest_framework.renderers.BrowsableAPIRenderer',)
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

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


STATIC_URL = env_var['Static']['STATIC_URL']
MEDIA_ROOT = env_var['Static']['MEDIA_ROOT']
MEDIA_URL = env_var['Static']['MEDIA_URL']
STATIC_ROOT = env_var['Static']['STATIC_ROOT']



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
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
#EMAIL_FILE_PATH = '/emails/'
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
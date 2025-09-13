from os import path, getenv
from dotenv import load_dotenv
from pathlib import Path



# Base Dir
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


# Load envs files
local_env_file = path.join(BASE_DIR, '.envs', '.env.local')
if path.isfile(local_env_file):
    load_dotenv(local_env_file)



# Application definition
LOCAL_APPS = ['core_apps.user', 'core_apps.voting', 'core_apps.candidate', 'core_apps.votes']

THIRD_PARTY_APPS  = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS 





# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('DB_NAME'),
        'HOST': getenv('DB_HOST'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'PORT': getenv('DB_PORT'),
        'OPTIONS':{
                'init_command':  "SET sql_mode='STRICT_ALL_TABLES', default_storage_engine=INNODB ",
                },
            }
        }




# Auth user model
AUTH_USER_MODEL = 'user.Users'



# Middwares 

LOCAL_MIDDLEWARE = ['core_apps.user.middleware.CheckUserRequestMiddleware',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] #+ LOCAL_MIDDLEWARE






# Media root 
MEDIA_DIR = '/media/'

MEDIA_URL = '/media/'

MEDIA_ROOT = path.join(BASE_DIR , "media")




# Static files 
STATIC_URL = 'static/'

STATICFILES_DIRS  = [path.join(BASE_DIR, 'static')]


























ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR , 'template'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

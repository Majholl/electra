from .base import * #noqa

from pathlib import Path 
from os import path , getenv
from dotenv import load_dotenv 
from datetime import timedelta
import json


SECRET_KEY = getenv("SECRET_KEY")

DEBUG = getenv("DEBUG")

ALLOWED_HOSTS = json.loads(getenv("ALLOWED_HOST",))

OTP_REQUIRED = getenv("OTP_REQUIRED")

CSRF_TRUSTED_ORIGINS = json.loads(getenv("CSRF_TRUSTED_ORIGINS"))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', ['https','http'])


OTP_EXPIRE_TIME = timedelta(minutes=5)

SESSION_COOKIE_AGE = int(getenv("SESSION_COOKIE_AGE"))


CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

CELERY_ACCEPT_CONTENT = ["application/json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = getenv('EMAIL_HOST')

EMAIL_PORT = getenv('EMAIL_PORT')

ADMIN_EMAIL=getenv('ADMIN_EMAIL')

DEFAULT_FROM_EMAIL=getenv('DEFAULT_FROM_EMAIL')
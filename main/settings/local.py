from .base import * #noqa

from pathlib import Path 
from os import path , getenv
from dotenv import load_dotenv 
from datetime import timedelta




SECRET_KEY = getenv("SECRET_KEY")

DEBUG = getenv("DEBUG")

ALLOWED_HOSTS = getenv("ALLOWED_HOST")

OTP_REQUIRED = getenv("OTP_REQUIRED")

CSRF_TRUSTED_ORIGINS = getenv("CSRF_TRUSTED")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

OTP_EXPIRE_TIME = timedelta(minutes=5)

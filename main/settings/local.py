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

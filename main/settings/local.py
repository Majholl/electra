from .base import * #noqa

from pathlib import Path 
from os import path , getenv
from dotenv import load_dotenv 
from datetime import timedelta




SECRET_KEY = getenv("SECRET_KEY")

DEBUG = getenv("DEBUG")

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

OTP_REQUIRED = getenv('OTP_REQUIRED')

OTP_EXPIRE_TIME = timedelta(minutes=5)

from pathlib import Path 
from os import path , getenv
from dotenv import load_dotenv 
from .base import * #noqa




SECRET_KEY = getenv("SECRET_KEY")

DEBUG = getenv("DEBUG")

ALLOWED_HOSTS = []
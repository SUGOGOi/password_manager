from .base import *
import os
from urllib.parse import urlparse, parse_qsl
from dotenv import load_dotenv


load_dotenv()


DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database - neon db
# Ensure we have a string to parse, defaulting to an empty string if None
db_url = os.getenv("DATABASE_URL", "")
tmpPostgres = urlparse(db_url)

# Convert attributes explicitly to strings to satisfy the type checker
db_path = str(tmpPostgres.path)
db_query = str(tmpPostgres.query)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db_path.replace("/", ""),
        "USER": tmpPostgres.username,
        "PASSWORD": tmpPostgres.password,
        "HOST": tmpPostgres.hostname,
        "PORT": 5432,
        "OPTIONS": dict(parse_qsl(db_query)),
        "CONN_HEALTH_CHECKS": True,
        "CONN_MAX_AGE": 600,
    }
}

# CORS — allow frontend dev server
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React default
    "http://localhost:5173",  # Vite default
]
CORS_ALLOW_CREDENTIALS = True  # ← required for cookies to work cross-origin


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # your gmail
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # gmail app password

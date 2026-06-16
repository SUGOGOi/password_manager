from pathlib import Path
import os
from dotenv import load_dotenv

# from django.templatetags.static import static
from django.urls import reverse_lazy


load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = []

# Default Django apps + our apps
INSTALLED_APPS = [
    "unfold.contrib.filters",  # optional — better filter UI
    "unfold.contrib.forms",  # optional — styled forms
    "unfold.contrib.inlines",  # optional — styled inlines
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # required by allauth
    # Third party
    "corsheaders",
    "ninja",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Our apps (we'll create these next)
    "apps.users",
    "apps.password_manager",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ← first!
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # required by allauth
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "core.asgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Allauth settings
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_EMAIL_VERIFICATION = "none"  # change to "mandatory" in prod

AUTH_USER_MODEL = "users.User"

SOCIALACCOUNT_AUTO_SIGNUP = True  # auto create user on first login
SOCIALACCOUNT_LOGIN_ON_GET = True  # ← skip confirmation page, go straight to Google
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_LOGIN_METHODS = ["email"]
# SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
# SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True


LOGIN_REDIRECT_URL = "/api/v1/auth/google/callback"
ADMIN_URL = "admin/"
# Keep admin login separate from allauth
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False


# OTP settings
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
ACCOUNT_CONFIRM_EMAIL_ON_GET = False

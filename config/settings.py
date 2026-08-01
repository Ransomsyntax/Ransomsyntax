"""
Django settings for the unified RansomSyntax platform.

This project merges two previously separate Django codebases:
  - the RansomSyntax marketing website (served at "/")
  - the RANSOM SYNTAX education platform (served at "/students/")

Configuration is environment-driven so the same codebase can run in
development and production. Copy `.env.example` to `.env` and adjust
values for your environment — see README.md for details.
"""

import os
from pathlib import Path

try:
    # python-dotenv is optional in production (real env vars may be used
    # instead) but convenient for local development.
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


# ---------------------------------------------------------------------------
# Core / security
# ---------------------------------------------------------------------------

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-CHANGE-ME-in-production-55e2f-jdr1-example-key",
)

DEBUG = env_bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost,.onrender.com,.vercel.app"
    ).split(",")
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Education platform apps (formerly the standalone "suryamaxcode" project)
    "accounts.apps.AccountsConfig",
    "courses.apps.CoursesConfig",
    "core.apps.CoreConfig",
    "chatbot.apps.ChatbotConfig",
    # Main marketing website app (kept last so its admin branding /
    # dashboard customizations are applied last and take precedence)
    "website.apps.WebsiteConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Site-wide constants (company name, contact email, social
                # links, tagline) available in every template. A single
                # shared context processor now covers both the main site
                # and the education platform, replacing the two separate
                # (but near-identical) processors each project used to have.
                "website.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

# The education platform's custom User model (student / teacher roles) is
# used project-wide. The main website's models (Service, Course,
# ClientEnquiry) have no relationship to the user model, so this is a
# drop-in shared setting with no data-model conflicts.
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Login redirects (education platform)
LOGIN_URL = "accounts:student_login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 200  # 200MB, needed for course video uploads
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 200

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Email (used for the client enquiry form notifications)
# ---------------------------------------------------------------------------

EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_bool("DJANGO_EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "no-reply@ransomsyntax.com")

# Where enquiry notifications are sent. Defaults to the company inbox.
ENQUIRY_NOTIFICATION_EMAIL = os.environ.get(
    "ENQUIRY_NOTIFICATION_EMAIL", "suryamaxcode@gmail.com"
)

# ---------------------------------------------------------------------------
# Site-wide constants (company profile, surfaced via context processor)
# ---------------------------------------------------------------------------

SITE_NAME = "RansomSyntax"
SITE_TAGLINE = "Engineering enterprise software with precision and craft."
SITE_CONTACT_EMAIL = "ransomsyntax@gmail.com"
SITE_YOUTUBE_URL = "https://www.youtube.com/@learn_your_skills"
SITE_INSTAGRAM_URL = "https://www.instagram.com/learn_your_skills/"

# Security hardening that only makes sense once DEBUG is off / TLS exists.
if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    X_CONTENT_TYPE_OPTIONS = "nosniff"

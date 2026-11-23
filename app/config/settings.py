import os
from pathlib import Path

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

# settings.py está en <raíz>/app/config/, así que la raíz queda 3 niveles arriba
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

DEBUG = os.getenv("DEBUG", "true").strip().lower() in {"1", "true", "yes", "on"}
SECRET_KEY = os.getenv("SECRET_KEY") or "dev-no-usar-en-produccion"
if not DEBUG and SECRET_KEY == "dev-no-usar-en-produccion":
    raise ImproperlyConfigured("Configura SECRET_KEY en el entorno cuando DEBUG esté desactivado.")
ALLOWED_HOSTS = [
    host.strip()
    for host in (os.getenv("ALLOWED_HOSTS") or "localhost,127.0.0.1").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "app.config.urls"
WSGI_APPLICATION = "app.config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app" / "vista"],   # tus HTML viven en app/vista
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

if os.getenv("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER", ""),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_USER_MODEL = "app.Usuario"   # nuestro modelo reemplaza al usuario de Django
LOGIN_URL = "login"

LANGUAGE_CODE = "es-pe"
TIME_ZONE = "America/Lima"
USE_TZ = True

# Mantiene las rutas que ya tienes en el HTML: /app/static/css/estilos.css
STATIC_URL = "/app/static/"
STATICFILES_DIRS = [BASE_DIR / "app" / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

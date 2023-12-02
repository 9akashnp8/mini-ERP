from .defaults import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

db_engine = env.str("DB_ENGINE")  # noqa: F405
if db_engine == "sqlite":
    DATABASES = {
        "default": env.dj_db_url("DATABASE_URL")  # noqa: F405
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "minierp_db",
            "USER": "minierp_user",
            "PASSWORD": "minierp_password",
            "HOST": "localhost",
        }
    }

# DRF Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": ("api.custom_pagination.FullResultsSetPagination"),
    "PAGE_SIZE": 10,
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_VERSION": "1",
    "ALLOWED_VERSIONS": ["1", "2"],
}

STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]  # noqa: F405
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))  # noqa: F405

CELERY_BROKER_URL = "redis://localhost:6379"

# CSRF Setting
CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]

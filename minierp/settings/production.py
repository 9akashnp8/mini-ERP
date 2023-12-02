from .defaults import *  # noqa : F403

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

ALLOWED_HOSTS = ["erp.lakshyaca.com", "www.erp.lakshyaca.com", "localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("DB_NAME"),  # noqa: F405
        "USER": env.str("DB_USER"),  # noqa: F405
        "PASSWORD": env.str("DB_USER_PASS"),  # noqa: F405
        "HOST": "localhost",
        "PORT": "",
    }
}

# DRF Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "api.custom_pagination.FullResultsSetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_VERSION": "1",
    "ALLOWED_VERSIONS": ["1", "2"],
}

SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(days=1)}  # noqa: F405

STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))  # noqa: F405

CELERY_BROKER_URL = f"redis://default:{env.str('REDIS_PASS')}@127.0.0.1:6379"  # noqa: F405

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/var/log/django/django.log",
            "formatter": "verbose",
        }
    },
    "loggers": {"django": {"handlers": ["file"], "level": "INFO", "propogate": True}},
}

sentry_sdk.init(
    dsn=env.str("SENTRY_DSN"),  # noqa: F405
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

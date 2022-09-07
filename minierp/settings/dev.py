from .defaults import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': env.dj_db_url("DATABASE_URL")
}

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

CELERY_BROKER_URL = "redis://localhost:6379"
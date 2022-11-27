from .defaults import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

db_engine = env.str("DB_ENGINE")
if db_engine == 'sqlite':
    DATABASES = {
        'default': env.dj_db_url("DATABASE_URL")
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'test_db'
        }
    }

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

CELERY_BROKER_URL = "redis://redis:6379"
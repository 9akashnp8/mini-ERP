from .defaults import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

db_engine = env.str("DB_ENGINE")  # noqa: F405
if db_engine == 'sqlite':
    DATABASES = {
        'default': env.dj_db_url("DATABASE_URL")  # noqa: F405
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost'
        }
    }

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]  # noqa: F405
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))  # noqa: F405

CELERY_BROKER_URL = "redis://localhost:6379"

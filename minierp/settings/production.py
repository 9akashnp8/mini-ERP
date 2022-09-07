from .defaults import *

DEBUG = False

ALLOWED_HOSTS = ['erp.lakshyaca.com', 'www.erp.lakshyaca.com', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str("DB_NAME"),
        'USER': env.str("DB_USER"),
        'PASSWORD': env.str("DB_USER_PASS"),
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

CELERY_BROKER_URL = f"redis://default:{env.str('REDIS_PASS')}@127.0.0.1:6379"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/django.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propogate': True
        }
    }
}
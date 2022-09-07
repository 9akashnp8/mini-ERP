from environs import Env
env = Env()
env.read_env()

ENVIRONMENT = env.str("ENVIRONMENT")

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .dev import *
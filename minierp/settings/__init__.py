from .base import *

from environs import Env

env = Env()
env.read_env()

if env.str('ENVIRONMENT') == 'prod':
    from .prod import *
else:
    from .dev import *
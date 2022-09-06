from .base import *

if env.str('ENVIRONMENT') == 'prod':
    from .prod import *
else:
    from .dev import *
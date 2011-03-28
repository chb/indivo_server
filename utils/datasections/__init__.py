import os
import sys
from django.core.management import setup_environ

UP = '../'
DISTANCE_FROM_HOME = 2

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + \
                    ''.join([UP for i in xrange(DISTANCE_FROM_HOME)])))

import settings
setup_environ(settings)

from accounts         import *
from auth_systems     import *
from document_schemas import *
from machine_apps     import *
from status_names     import *
from user_apps        import *

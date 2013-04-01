import os
import sys

UP = '../'
DISTANCE_FROM_HOME = 2

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/' + \
                    ''.join([UP for i in xrange(DISTANCE_FROM_HOME)])))


os.environ['DJANGO_SETTINGS_MODULE'] = 'indivo.settings'

from accounts         import *
from auth_systems     import *
from document_schemas import *
from status_names     import *

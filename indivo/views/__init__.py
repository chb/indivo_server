""" Indivo Views """

VERSION = '0.9.3.0'

from account    import *
from audit      import *
from documents  import *
from messaging  import *
from pha        import *
from record     import *
from reports    import *
from shares     import *

from django.http import HttpResponse
def get_version(request): return HttpResponse(VERSION, mimetype="text/plain")

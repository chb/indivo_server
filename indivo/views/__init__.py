""" Indivo Views """

from ..version import INDIVO_SERVER_VERSION, INDIVO_SERVER_RELEASE

from account    import *
from audit      import *
from documents  import *
from messaging  import *
from pha        import *
from record     import *
from reports    import *
from shares     import *

from django.http import HttpResponse
def get_version(request): return HttpResponse(INDIVO_SERVER_RELEASE, 
                                              mimetype="text/plain")

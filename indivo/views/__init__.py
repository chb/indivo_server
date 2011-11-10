""" Indivo Views.
The Django views that implement all Indivo API functionality,
including API calls related to:

* accounts
* auditing
* documents
* messaging
* apps
* records
* reporting
* sharing
"""

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
def get_version(request): 
    """ Return the current version of Indivo."""
    return HttpResponse(INDIVO_SERVER_RELEASE, mimetype="text/plain")

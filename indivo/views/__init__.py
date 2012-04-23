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

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from version import INDIVO_SERVER_VERSION, INDIVO_SERVER_RELEASE, SMART_COMPATIBILITY

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
    return HttpResponse(_get_version(), mimetype="text/plain")


def _get_version():
    return INDIVO_SERVER_RELEASE

def _get_smart_version(indivo_version):
    if SMART_COMPATIBILITY.has_key(indivo_version):
        return SMART_COMPATIBILITY[indivo_version]
    return ''

def _get_indivo_version(smart_version):
    for k,v in SMART_COMPATIBILITY.iteritems():
        if v == smart_version:
            return k

    return None

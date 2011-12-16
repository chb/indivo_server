"""
Middleware (filters) for Indivo

inspired by django.contrib.auth middleware, but doing it differently
for tighter integration into email-centric users in Indivo.
"""

from indivo.accesscontrol import security
from indivo.lib.utils import DjangoVersionDependentExecutor

class Authentication(object):
  def process_request(self, request):

    # django 1.3.0 fails to create a QueryDict for request.POST if we access
    # request.raw_post_data first, but django 1.3.1 raises an exception if
    # we read request.POST and subsequently read request.raw_post_data.
    #
    # So, we preemptively read the appropriate variable first, depending on
    # the current version of django
    self.avoid_post_clobbering(request)

    request.principal, request.oauth_request = security.get_principal(request)

  
  noclobber_map = {'1.3.0': lambda request: request.POST,
                   '1.3.1+': lambda request: request.raw_post_data,
                   }
  avoid_post_clobbering = DjangoVersionDependentExecutor(noclobber_map)

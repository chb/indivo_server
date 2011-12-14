"""
Middleware (filters) for Indivo

inspired by django.contrib.auth middleware, but doing it differently
for tighter integration into email-centric users in Indivo.
"""

from indivo.accesscontrol import security

class LazyUser(object):
  def __get__(self, request, obj_type = None):
    if not hasattr(request, '_cached_user'):
      request._cached_user = auth.get_user(request)
    return request._cached_user

class Authentication(object):
  def process_request(self, request):

    # django 1.3 fails to create a QueryDict for request.POST if we access
    # request.raw_post_data first. So, we preemptively read request.POST
    # before oauth libraries read request.raw_post_data ...
    noclobber = request.POST

    request.principal, request.oauth_request = security.get_principal(request)

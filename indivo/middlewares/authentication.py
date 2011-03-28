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
    request.principal, request.oauth_request = security.get_principal(request)

"""
Middleware (filters) for Indivo

inspired by django.contrib.auth middleware, but doing it differently
for tighter integration into email-centric users in Indivo.
"""

import re
import indivo

from time import strftime
from django.http import *
from django.core.exceptions import PermissionDenied
from django.conf import settings
from indivo.accesscontrol.access_rule import AccessRule

class Authorization(object):

  def process_view(self, request, view_func, view_args, view_kwargs):
    """ The process_view() hook allows us to examine the request before view_func is called"""
    # Special override flag
    if self.OVERRIDE:
      return None

    # Url exception(s)
    exc_pattern= settings.INDIVO_ACCESS_CONTROL_EXCEPTION
    if exc_pattern and re.match(exc_pattern, request.path):
      return None
 
    if hasattr(view_func, 'resolve'):
      view_func = view_func.resolve(request)

    try:
      if view_func and self.valid_principal_p(request):
        access_rule = self.get_access_rule(view_func)

        if access_rule and access_rule.check(request.principal, **view_kwargs): 
          return None # Accept
    except:
      raise PermissionDenied
    raise PermissionDenied

  def valid_principal_p(self, request):
    return hasattr(request, 'principal') and request.principal

  def get_access_rule(self, view_func):
    return AccessRule.lookup(view_func)

  @classmethod
  def override(cls):
    cls.OVERRIDE = True

Authorization.OVERRIDE = False

# Mark that the authorization module has been loaded
# nothing gets served otherwise
indivo.AUTHORIZATION_MODULE_LOADED = True

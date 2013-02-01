"""
Authentication for Indivo
"""

from django.http import HttpResponse, HttpResponseRedirect, Http404
import functools, urllib
from django.core.exceptions import PermissionDenied
from indivo import models

USER_ID = "_user_id"
NUM_LOGIN_ATTEMPTS = '_num_login_attempts'

def authenticate(request, username, password=None, system=None):
  """Check credentials

  """
  try:
    if password:
      user = models.AccountAuthSystem.objects.get( 
          auth_system = models.AuthSystem.PASSWORD(), 
          username    = urllib.unquote(username).lower().strip()).account
      if user.is_active and user.password_check(password):
        user.on_successful_login()
        return user
      else:
        user.on_failed_login()
        raise PermissionDenied()
    elif system:
      user = models.AccountAuthSystem.objects.get( 
          auth_system = models.AuthSystem.objects.get(short_name=system), 
          username    = urllib.unquote(username).lower().strip()).account
      if user.is_active:
        return user
      else:
        raise PermissionDenied()
  except:
    raise PermissionDenied()
  return False

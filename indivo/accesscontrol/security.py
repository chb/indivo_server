"""
A number of security utilities for Indivo

based on django constructs
and Indivo data models
"""

from django.core.exceptions import *

import functools, copy, logging

from oauth import oauth, djangoutils

from indivo import models
from indivo.accesscontrol.oauth_servers import ADMIN_OAUTH_SERVER, OAUTH_SERVER, SESSION_OAUTH_SERVER

##
## Gather information about the request
##

def get_chrome_user_session_info(request):
  try:
    oauth_request = SESSION_OAUTH_SERVER.extract_oauth_request(djangoutils.extract_request(request))
    consumer, token, parameters = SESSION_OAUTH_SERVER.check_resource_access(oauth_request)
    return consumer, token, parameters, oauth_request
  except oauth.OAuthError:
    return None, None, None, None


def get_user_app_info(request):
  try:
    oauth_request = OAUTH_SERVER.extract_oauth_request(djangoutils.extract_request(request))
    consumer, token, parameters = OAUTH_SERVER.check_resource_access(oauth_request)
    return consumer, token, parameters, oauth_request
  except oauth.OAuthError:
    return None, None, None, None

def get_admin_app_info(request):
  try:
    oauth_request = ADMIN_OAUTH_SERVER.extract_oauth_request(djangoutils.extract_request(request))
    admin_app, null_token, parameters = ADMIN_OAUTH_SERVER.check_resource_access(oauth_request)
    return admin_app, null_token, parameters, oauth_request
  except:
    return None, None, None, None

def get_record_by_id(id):
  try:
    return models.Record.objects.get(id=id)
  except models.Record.DoesNotExist:
    return None

def get_pha_by_email(email):
  return models.PHA.objects.get(email = email)

def get_principal(request):
  """Figure out the principal making the request.

  First web user, then PHA, then Chrome App sudo'ing.

  """

  # is this a chrome app with a user session token?
  chrome_app, token, parameters, oauth_request = get_chrome_user_session_info(request)
  if token:
    return token.user, oauth_request
  
  # check oauth
  # IMPORTANT: the principal is the token, not the PHA itself
  # TODO: is this really the right thing, is the token the principal?
  pha, token, parameters, oauth_request = get_user_app_info(request)
  if pha:
    if token:
      return token, oauth_request
    else:
      return pha, oauth_request

  # check a machine application
  admin_app, token, params, oauth_request = get_admin_app_info(request)

  if admin_app:
    return admin_app, oauth_request

  # is this an admin login?
  if not request.META.has_key('HTTP_AUTHORIZATION') and request.user.is_authenticated():
    return models.AdminUser.objects.get_or_create(email=request.user.email)[0], None

  # No auth--return the NoUser type.
  return models.NoUser.get_nouser(), None


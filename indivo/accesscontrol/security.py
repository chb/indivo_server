"""
A number of security utilities for Indivo

based on django constructs
and Indivo data models
"""

from django.core.exceptions import *

import functools, copy, logging

from oauth import oauth, djangoutils

from indivo import models
from indivo.accesscontrol.oauth_servers import ADMIN_OAUTH_SERVER, OAUTH_SERVER, SESSION_OAUTH_SERVER, CONNECT_OAUTH_SERVER

##
## Gather information about the request
##

def get_oauth_info(request, server):
  try:
    oauth_request = server.extract_oauth_request(djangoutils.extract_request(request))
    consumer, token, parameters = server.check_resource_access(oauth_request)
    return consumer, token, parameters, oauth_request
  except oauth.OAuthError as e:
    return None, None, None, None

def get_principal(request):
  """Figure out the principal making the request.

  First PHA authenticated via Connect, then web user, then PHA, then Chrome App sudo'ing.

  """

  # is this a Connect-style authentication for an app?
  chrome_app, token, parameters, oauth_request = get_oauth_info(request, CONNECT_OAUTH_SERVER)
  if chrome_app and token:
    return token, oauth_request

  # is this a chrome app with a user session token?
  chrome_app, token, parameters, oauth_request = get_oauth_info(request, SESSION_OAUTH_SERVER)
  if token:
    return token.user, oauth_request
  
  # is this a userapp, either two-legged or authorized by the user?
  # IMPORTANT: the principal is the token, not the PHA itself
  # TODO: is this really the right thing, is the token the principal?
  pha, token, parameters, oauth_request = get_oauth_info(request, OAUTH_SERVER)
  if pha:
    if token:
      return token, oauth_request
    else:
      return pha, oauth_request

  # check a machine application
  admin_app, token, params, oauth_request = get_oauth_info(request, ADMIN_OAUTH_SERVER)
  if admin_app:
    return admin_app, oauth_request

  # is this a 'no-user' login?
  if not request.META.has_key('HTTP_AUTHORIZATION'):

    # Only 1 NoUser principal in the database: create it if it
    # doesn't yet exist
    try:
      no_user = models.NoUser.objects.all()[0]
    except IndexError:
      no_user = models.NoUser.objects.create(email="", type='NoUser')
    return no_user, None

  return None, None


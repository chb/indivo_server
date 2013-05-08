"""
Middleware (filters) for Indivo

inspired by django.contrib.auth middleware, but doing it differently
for tighter integration into email-centric users in Indivo.
"""

from indivo.accesscontrol import security

class Authentication(object):

  def process_request(self, request):
    request.principal, request.oauth_request = security.get_principal(request)
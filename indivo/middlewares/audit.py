"""
Middleware (filters) for Indivo

inspired by django.contrib.auth middleware, but doing it differently
for tighter integration into email-centric users in Indivo.
"""

import sys, logging
from indivo.accesscontrol import security
from indivo.models import Audit, Principal, Record, Document
from time import strftime
from django.http import *
from django.conf import settings

# AUDIT DATA CATEGORIES:
BASIC = 'basic' # REQUIRED, if audit_level > 'NONE': basic info about request
PRINCIPAL_INFO = 'principal_info' # identifier of principal making request
RESOURCES = 'resources' # resources accessed by request
REQUEST_INFO = 'request_info' # Data passed in through the request (headers, ip, domain, etc.)
RESPONSE_INFO = 'response_info' # Response code, error messages, etc.

AUDIT_LEVELS = {
  'NONE': [],
  'LOW': [BASIC, PRINCIPAL_INFO],
  'MED': [BASIC, PRINCIPAL_INFO, RESOURCES],
  'HIGH': [BASIC, PRINCIPAL_INFO, RESOURCES, REQUEST_INFO, RESPONSE_INFO]
}

class AuditWrapper(object):
  """
  Audit...
  """

  # DH 04-25-2011: Not sure what this was for--let's try getting rid of it.
  #def process_request(self, request):
  #  if not request.principal:
  #    try:
  #      request.principal, request.oauth_request = security.get_principal(request)
  #    except:
        # to get around an annoying bug for now, when auth fails
  #      pass

  def __init__(self):
    # get Audit related settings
    self.audit_level = settings.AUDIT_LEVEL
    self.audit_oauth = settings.AUDIT_OAUTH
    self.audit_failure = settings.AUDIT_FAILURE
    if not AUDIT_LEVELS.has_key(self.audit_level):
      raise Exception('Invalid audit level in settings.py: %s'%(self.audit_level))

    self.audit_obj = None

  def must_audit(self, request):
    if self.audit_level == 'None':
      return False
    return self.audit_oauth or (not request.META['PATH_INFO'].startswith('/oauth'))

  def process_view(self, request, view_func, view_args, view_kwargs):
    basic = {}
    principal_info = {}
    resources = {}
    request_info = {}

    # Don't audit unless required to
    if not self.must_audit(request):
      self.audit_obj = None
      return None

    # Basic Info
    basic['datetime'] = strftime("%Y-%m-%d %H:%M:%S")

    if hasattr(view_func, 'resolve'):
      view_func = view_func.resolve(request)
    basic['view_func'] = view_func.func_name

    # Principal Info
    if request.principal:
      principal_info['effective_principal_email'] = request.principal.effective_principal.email
      proxied_by = request.principal.proxied_by
      if proxied_by:
        principal_info['proxied_by_email'] = proxied_by.email

    # Resources
    carenet_id = record_id = None
    if view_kwargs.has_key('record'):
      resources['record_id'] = view_kwargs['record'].id
    elif view_kwargs.has_key('carenet'):
      resources['carenet_id'] = view_kwargs['carenet'].id

    if view_kwargs.has_key('document_id'):
      resources['document_id'] = view_kwargs['document_id']

    if view_kwargs.has_key('external_id'):

      # No need to resolve external ids: the info will still be in the DB
      resources['external_id'] = view_kwargs['external_id']
      
    if view_kwargs.has_key('message_id'):
      resources['message_id'] = view_kwargs['message_id']

    if view_kwargs.has_key('pha'):
      resources['pha_id'] = view_kwargs['pha'].id

    # Request Info

    # if request.META contains HTTP_AUTHORIZATION then use it
    # SZ: Temporary solution
    # Due to the possibility of different standards
    # we will need to check request.META
    # abstract this out!
    req_headers = ''
    if request.META.has_key('HTTP_AUTHORIZATION'):
      req_headers = request.META['HTTP_AUTHORIZATION']
    remote_host = ''
    if request.META.has_key('REMOTE_HOST'):
      remote_host = request.META['REMOTE_HOST']
    request_info['req_domain'] = remote_host
    request_info['req_headers'] = req_headers
    request_info['req_method'] = request.META['REQUEST_METHOD']
    request_info['req_ip_address'] = request.META['REMOTE_ADDR']
    request_info['req_url'] = request.META['PATH_INFO']

    # Build Audit object based on audit level
    data = {}
    for data_category in AUDIT_LEVELS[self.audit_level]:
      if data_category == BASIC:
        data.update(basic)
      if data_category == PRINCIPAL_INFO:
        data.update(principal_info)
      elif data_category == RESOURCES:
        data.update(resources)
      elif data_category == REQUEST_INFO:
        data.update(request_info)
      else:
        pass # ignore data categories we don't know about

    self.audit_obj = Audit(**data) if data else None
    
    return None

  def process_response(self, request, response):

    # Don't audit unless required to
    if not self.must_audit(request):
      return response

    # Build up data
    content_type = 'text/plain'
    content_type_str = 'content-type'

    status_code = 500
    if hasattr(response, 'status_code'):
      status_code = response.status_code

    if hasattr(response, '_headers') and \
        response._headers.has_key(content_type_str) and \
        response._headers[content_type_str][1]:
      content_type = response._headers[content_type_str][1]

    # Did the request complete successfully
    request_successful =  status_code < 400

    data = {}
    for data_category in AUDIT_LEVELS[self.audit_level]:
      if data_category == BASIC:
        data['request_successful'] = request_successful
    
      elif data_category == RESPONSE_INFO:
        data['resp_code'] = status_code
        data['resp_headers'] = content_type
        # Add error message in here mabye

    # Don't audit if we failed and aren't auditing failures
    if self.audit_failure or status_code < 400:
      self.save_response(data)

    if status_code == 403:
      logging.error("permission denied")
      from django import http
      return http.HttpResponseForbidden("<h4>Permission Denied</h4>")

    return response

  def save_response(self, data):
    if not self.audit_obj and data:
      # We got an exception before hitting auditwrapper on the way in: make sure to add basic info
      data['datetime'] = strftime("%Y-%m-%d %H:%M:%S")
      self.audit_obj = Audit(**data)

    else:
      for k,v in data.iteritems():
        if hasattr(self.audit_obj, k):
          setattr(self.audit_obj, k, v)
        
    self.audit_obj.save()

  def process_exception(self, request, exception):
    print >> sys.stderr, exception
    sys.stderr.flush()

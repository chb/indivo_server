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

class AuditWrapper(object):
  """
  Audit...
  """

  def process_request(self, request):
    if not request.principal:
      try:
        request.principal, request.oauth_request = security.get_principal(request)
      except:
        # to get around an annoying bug for now, when auth fails
        pass

  def process_view(self, request, view_func, view_args, view_kwargs):

    # no longer needed
    # principal_id, principal_email, principal_creator, principal_type = self.get_principal(request.principal)

    
    proxied_by_email = None
    effective_principal_email = None
    
    if request.principal:
      effective_principal_email = request.principal.effective_principal.email
      proxied_by = request.principal.proxied_by
      if proxied_by:
        proxied_by_email = proxied_by.email

    ids = self.resolve_external_id(view_kwargs)
    record_id = ids['record_id']
    document_id =  ids['document_id']
    now = strftime("%Y-%m-%d %H:%M:%S")

    if hasattr(view_func, 'resolve'):
      view_func = view_func.resolve(request)

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

    # Insert into Audit
    # Ben 2010-01-19: simpler fix for func name.
    self.audit_obj = Audit.objects.create(  req_view_func = view_func.func_name,
                                            req_url=request.META['PATH_INFO'],
                                            req_datetime=now,
                                            req_ip_address=request.META['REMOTE_ADDR'],
                                            req_domain=remote_host,
                                            req_headers=req_headers,
                                            req_method=request.META['REQUEST_METHOD'],
                                            # req_principal_id=principal_id,
                                            # req_principal_email=principal_email,
                                            # req_principal_creator_email=principal_creator,
                                            # req_principal_type=principal_type,
                                            req_effective_principal_email = effective_principal_email,
                                            req_proxied_by_principal_email = proxied_by_email,
                                            resp_code=200,
                                            record=record_id,
                                            document=document_id)

  ## MAY NO LONGER BE NEEDED (Ben 2010-01-19)
  def get_principal(self, principal):
    # Get the id and creator of the principal
    principal_id = ''
    principal_email = ''
    principal_creator = ''
    principal_type = ''
    if principal:
      if hasattr(principal, 'id') and \
         principal.id:
        principal_id = principal.id
      if hasattr(principal, 'email'):
        principal_email = principal.email
      if hasattr(principal, 'creator') and \
        principal.creator:
        principal_creator = Principal.objects.get(id=principal.creator.id).email
      if hasattr(principal, '__class__()') and \
          hasattr(principal.__class__(), '__repr__()'):
        principal_type = principal.__class__().__repr__()
    return principal_id, principal_email, principal_creator, principal_type

  def resolve_external_id(self, view_kwargs):
    # FIXME: is this working with external IDs?
    # I don't think so.
    # I'm also concerned about doing DB queries in the auditing portion (Ben 2010-08-15)
    record_id_str     = 'record_id'
    document_id_str   = 'document_id'
    app_email_str     = 'app_email'
    external_id_str   = 'external_id'
    res = {record_id_str : '', document_id_str : ''}
    kwargs_obj = {record_id_str : Record, document_id_str : Document}
    externalid_exists = view_kwargs.has_key(app_email_str) and view_kwargs.has_key(external_id_str)
    for kwarg, obj in kwargs_obj.items():
      if not view_kwargs.has_key(kwarg):
        if externalid_exists:
          res[kwarg] = obj.objects.get(external_id=view_kwargs[kwarg]).id
      else:
        res[kwarg] = view_kwargs[kwarg]
    return res

  def process_response(self, request, response):
    content_type = 'text/plain'
    content_type_str = 'content-type'
    status_code = 500
    if hasattr(response, 'status_code'):
      status_code = response.status_code
    if hasattr(response, '_headers') and \
        response._headers.has_key(content_type_str) and \
        response._headers[content_type_str][1]:
      content_type = response._headers[content_type_str][1]
    self.save_response(status_code, content_type)

    if status_code == 403:
      logging.error("permission denied")
      from django import http
      return http.HttpResponseForbidden("<h4>Permission Denied</h4>")

    return response

  def save_response(self, status_code, content_type, content=''):
    if hasattr(self, 'audit_obj'):
      self.audit_obj.resp_code      = status_code
      self.audit_obj.resp_headers   = content_type
      # SZ: For now, resp_error_msg will always be an empty string
      self.audit_obj.resp_error_msg = content
      self.audit_obj.save()

  # deprecated 2010-01-19: just use func.func_name
  def get_function_name(self, func_repr):
    try:
      nbsp = ' '
      search_str = 'at'
      func_repr = func_repr.strip()
      return func_repr[func_repr.find(nbsp):func_repr.find(nbsp + search_str + nbsp)]
    except:
      return func_repr

  def process_exception(self, request, exception):
    print >> sys.stderr, exception
    sys.stderr.flush()

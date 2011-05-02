"""
Indivo Views -- Auditing
"""

import logging, copy
from base import *
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import execute_query, render_results_template, DATE, STRING, NUMBER
from indivo.models import Audit
from django.http import HttpResponseBadRequest, HttpResponse

AUDIT_FILTERS = {
  'record_id': ('record_id', STRING),
  'document_id': ('document_id', STRING),
  'external_id': ('external_id', STRING),
  'request_date': ('datetime', DATE),
  'function_name': ('view_func', STRING),
  'principal_email':('effective_principal_email', STRING),
  'proxied_by_email': ('proxied_by_email', STRING),
  DEFAULT_ORDERBY: ('datetime', DATE),
}

AUDIT_TEMPLATE = 'audit.xml'

@marsloader(query_api_support=True)
def audit_query(request, group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record=None):
  '''Select Audit Objects via the Query API Interface'''
  try:
    query_filters = copy.copy(filters)
    if record:
      # Careful: security hole here.
      # /records/abc/audits/?record_id=bcd is dangerous
      # Eliminate that possibility
      if filters.has_key('record_id') and filters['record_id'] is not record.id:
        return HttpResponseBadRequest('Cannot make Audit queries over records not in the request url')

      query_filters['record_id'] = record.id

    results, trc, aggregate_p = execute_query(Audit, AUDIT_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              None, date_range, query_filters, # ignore status for audits
                                              record=None, carenet=None)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

  return render_results_template(results, trc, aggregate_p, AUDIT_TEMPLATE,
                                 group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters)


##################################
## DEPRECATED CALLS:             #
## Use Query API via audit_query #
##################################
@marsloader()
def audit_function_view(request, record, document_id, function_name, limit, offset, order_by, status=None):
  try:
    audits = Audit.objects.filter(record_id=record.id,
                                  document_id=document_id, 
                                  view_func=function_name).order_by('-datetime')[offset:offset+limit]
    return render_template('audit', {'audits' : audits}, type='xml')
  except:
    raise Http404


@marsloader()
def audit_record_view(request, record, limit, offset, order_by, status = None):
  try:
    audits = Audit.objects.filter(record_id=record.id).order_by('-datetime')[offset:offset+limit]
    return render_template('audit', {'audits' : audits}, type='xml')
  except:
    raise Http404


@marsloader()
def audit_document_view(request, record, document_id, limit, offset, order_by, status=None):
  try:
    audits = Audit.objects.filter(record_id=record.id,
                                  document_id=document_id).order_by('-datetime')[offset:offset+limit]
    return render_template('audit', {'audits' : audits}, type='xml')
  except:
    raise Http404

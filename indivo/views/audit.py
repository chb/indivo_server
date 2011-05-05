"""
Indivo Views -- Auditing
"""

import logging, copy
from base import *
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
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
  query_filters = copy.copy(filters)
  if record:
    # Careful: security hole here.
    # /records/abc/audits/?record_id=bcd is dangerous
    # Eliminate that possibility
    if filters.has_key('record_id') and filters['record_id'] is not record.id:
      return HttpResponseBadRequest('Cannot make Audit queries over records not in the request url')
    
    query_filters['record_id'] = record.id

  q = FactQuery(Audit, AUDIT_FILTERS,
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                None, date_range, query_filters, # ignore status for audits
                record=None, carenet=None)
  try:
    # Don't display record_id in the output if it wasn't in the query string.
    q.execute()
    if q.query_filters.has_key('record_id') and not filters.has_key('record_id'):
      del q.query_filters['record_id']
    
    return q.render(AUDIT_TEMPLATE)

  except ValueError as e:
    return HttpResponseBadRequest(str(e))

##################################
## DEPRECATED CALLS:             #
## Use Query API via audit_query #
##################################
@marsloader()
def audit_function_view(request, record, document_id, function_name, limit, offset, order_by, status=None):
  try:
    audits = Audit.objects.filter(record_id=record.id,
                                  document_id=document_id, 
                                  view_func=function_name).order_by('-datetime')
    return render_template('reports/report', 
                           {'fobjs' : audits[offset:offset+limit],
                            'trc': len(audits),
                            'item_template': AUDIT_TEMPLATE,
                            'limit': limit,
                            'offset': offset,
                            'order_by': order_by,
                            'status': status}, 
                           type='xml')
  except:
    raise Http404


@marsloader()
def audit_record_view(request, record, limit, offset, order_by, status = None):
  try:
    audits = Audit.objects.filter(record_id=record.id).order_by('-datetime')
    return render_template('reports/report', 
                           {'fobjs' : audits[offset:offset+limit],
                            'trc': len(audits),
                            'item_template': AUDIT_TEMPLATE,
                            'limit': limit,
                            'offset': offset,
                            'order_by': order_by,
                            'status': status}, 
                           type='xml')
  except:
    raise Http404


@marsloader()
def audit_document_view(request, record, document_id, limit, offset, order_by, status=None):
  try:
    audits = Audit.objects.filter(record_id=record.id,
                                  document_id=document_id).order_by('-datetime')
    return render_template('reports/report', 
                           {'fobjs' : audits[offset:offset+limit],
                            'trc': len(audits),
                            'item_template': AUDIT_TEMPLATE,
                            'limit': limit,
                            'offset': offset,
                            'order_by': order_by,
                            'status': status}, 
                           type='xml')
  except:
    raise Http404

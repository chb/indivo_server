"""
.. module:: views.audit
   :synopsis: Indivo view implementations for audit-related calls.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

import copy
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
def audit_query(request, query_options,
                record=None):
  """ Select Audit Objects via the Query API Interface.

  Accepts any argument specified by the :doc:`/query-api`, and filters
  available audit objects by the arguments.

  Will return :http:statuscode:`200` with XML containing individual or
  aggregated audit records on succes, :http:statuscode:`400` if any of 
  the arguments to the query interface are invalid.

  """
  query_filters = copy.copy(query_options['filters'])
  if record:
    # Careful: security hole here.
    # /records/abc/audits/?record_id=bcd is dangerous
    # Eliminate that possibility
    if query_filters.has_key('record_id') and query_filters['record_id'] is not record.id:
      return HttpResponseBadRequest('Cannot make Audit queries over records not in the request url')
    
    query_filters['record_id'] = record.id
    query_options['filters'] = query_filters
    query_options['status'] = None #ignore status for audits
    
  q = FactQuery(Audit, AUDIT_FILTERS,
                query_options,
                record=None, carenet=None)
  try:
    # Don't display record_id in the output if it wasn't in the query string.
    q.execute()
    if q.query_filters.has_key('record_id') and not query_options['filters'].has_key('record_id'):
      del q.query_filters['record_id']
    
    return q.render(AUDIT_TEMPLATE)

  except ValueError as e:
    return HttpResponseBadRequest(str(e))

##################################
## DEPRECATED CALLS:             #
## Use Query API via audit_query #
##################################
@marsloader()
def audit_function_view(request, record, document_id, function_name, query_options):
  """ Return audits of calls to *function_name* touching *record* and *document_id*.

  Will return :http:statuscode:`200` with matching audits on succes, 
  :http:statuscode:`404` if *record* or *document_id* don't exist.

  .. deprecated:: 0.9.3
     Use :py:meth:`~indivo.views.audit.audit_query` instead.

  """

  try:
    audits = Audit.objects.filter(record_id=record.id,
                                  document_id=document_id, 
                                  view_func=function_name).order_by('-datetime')
                                  
    offset = query_options['offset']
    limit = query_options['limit']
    order_by = query_options['order_by']
    status = query_options['status']
    total_result_count = audits.count()
    if limit:
        audits = audits[offset:offset+limit]
    return render_template('reports/report', 
                           {'fobjs' : audits,
                            'trc': total_result_count,
                            'item_template': AUDIT_TEMPLATE,
                            'limit': limit,
                            'offset': offset,
                            'order_by': order_by,
                            'status': status}, 
                           type='xml')
  except:
    raise Http404


@marsloader()
def audit_record_view(request, record, query_options):
  """ Return audits of calls touching *record*.

  Will return :http:statuscode:`200` with matching audits on succes, 
  :http:statuscode:`404` if *record* doesn't exist.

  .. deprecated:: 0.9.3
     Use :py:meth:`~indivo.views.audit.audit_query` instead.

  """
  offset = query_options['offset']
  limit = query_options['limit']
  order_by = query_options['order_by']
  status = query_options['status']
  try:
    audits = Audit.objects.filter(record_id=record.id).order_by('-datetime')
    total_result_count = audits.count()
    if limit:
        audits = audits[offset:offset+limit]
    return render_template('reports/report', 
                           {'fobjs' : audits,
                            'trc': total_result_count,
                            'item_template': AUDIT_TEMPLATE,
                            'limit': limit,
                            'offset': offset,
                            'order_by': order_by,
                            'status': status}, 
                           type='xml')
  except:
    raise Http404


@marsloader()
def audit_document_view(request, record, document_id, query_options):
  """ Return audits of calls touching *record* and *document_id*.

  Will return :http:statuscode:`200` with matching audits on succes, 
  :http:statuscode:`404` if *record* or *document_id* don't exist.

  .. deprecated:: 0.9.3
     Use :py:meth:`~indivo.views.audit.audit_query` instead.

  """

  try:
    audits = Audit.objects.filter(record_id=record.id,
                                  document_id=document_id).order_by('-datetime')
                                  
    offset = query_options['offset']
    limit = query_options['limit']
    order_by = query_options['order_by']
    status = query_options['status']
    total_result_count = audits.count()
    if limit:
        audits = audits[offset:offset+limit]
    return render_template('reports/report', 
                           {'fobjs' : audits,
                            'trc': total_result_count,
                            'item_template': AUDIT_TEMPLATE,
                            'limit': limit,
                            'offset': offset,
                            'order_by': order_by,
                            'status': status}, 
                           type='xml')
  except:
    raise Http404

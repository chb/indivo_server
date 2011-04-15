"""
Indivo Views -- Procedure
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.utils import render_template
from indivo.lib.query import execute_query, DATE, STRING, NUMBER
from indivo.models import Procedure

PROCEDURE_FILTERS = {
  'procedure_name' : ('name', STRING),
  'date_performed': ('date_resolution', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

def procedure_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _procedure_list"""
  return _procedure_list(*args, **kwargs)

def carenet_procedure_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _procedure_list"""
  return _procedure_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _procedure_list(request, group_by, date_group, aggregate_by,
                    limit, offset, order_by,
                    status, date_range, filters,
                    record=None, carenet=None):

  try:
    results, trc, aggregate_p = execute_query(Procedure, PROCEDURE_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))


  if aggregate_p:
    # Waiting on aggregate schema
    return HttpResponse(str(results))

  else:
    return render_template('reports/procedures', 
                           { 'procedures' : results,
                             'trc' : trc,
                             'limit' : limit,
                             'offset' : offset,
                             'order_by' : order_by}, 
                           type="xml")

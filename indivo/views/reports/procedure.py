"""
Indivo Views -- Procedure
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Procedure

PROCEDURE_FILTERS = {
  'procedure_name' : ('name', STRING),
  'date_performed': ('date_performed', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

PROCEDURE_TEMPLATE = 'reports/procedure.xml'

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

  q = FactQuery(Procedure, PROCEDURE_FILTERS,
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)

  try:
    return q.render(PROCEDURE_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

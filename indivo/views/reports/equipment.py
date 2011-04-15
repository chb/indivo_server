"""
Indivo Views -- Equipment
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.utils import render_template
from indivo.lib.query import execute_query, DATE, STRING, NUMBER
from indivo.models import Equipment

EQUIPMENT_FILTERS = {
  'date_started': ('date_started', DATE),
  'date_stopped': ('date_stopped', DATE),
  'equipment_name': ('name', STRING),
  'equipment_vendor': ('vendor', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

def equipment_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _equipment_list"""
  return _equipment_list(*args, **kwargs)


def carenet_equipment_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _equipment_list"""
  return _equipment_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _equipment_list(request, group_by, date_group, aggregate_by,
                       limit, offset, order_by,
                       status, date_range, filters,
                       record=None, carenet=None):


  try:
    results, trc, aggregate_p = execute_query(Equipment, EQUIPMENT_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))


  if aggregate_p:
    # Waiting on aggregate schema
    return HttpResponse(str(results))

  return render_template('reports/equipment', 
                          { 'equipment' : results,
                            'trc' : trc,
                            'limit' : limit,
                            'offset' : offset,
                            'order_by' : order_by },
                          type="xml")

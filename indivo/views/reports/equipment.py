"""
Indivo Views -- Equipment
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Equipment

EQUIPMENT_FILTERS = {
  'date_started': ('date_started', DATE),
  'date_stopped': ('date_stopped', DATE),
  'equipment_name': ('name', STRING),
  'equipment_vendor': ('vendor', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

EQUIPMENT_TEMPLATE = 'reports/equipment.xml'

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
  q = FactQuery(Equipment, EQUIPMENT_FILTERS,
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(EQUIPMENT_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

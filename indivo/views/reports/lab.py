"""
Indivo Views -- Lab
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Lab

LAB_FILTERS = {
  'lab_type': ('lab_type', STRING),
  'date_measured': ('date_measured', DATE),
  'lab_test_name': ('first_lab_test_name', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

LAB_TEMPLATE = 'reports/lab.xml'

def lab_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _lab_list"""
  return _lab_list(*args, **kwargs)

def carenet_lab_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _lab_list"""
  return _lab_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _lab_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  
  q = FactQuery(Lab, LAB_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(LAB_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

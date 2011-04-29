"""
Indivo Views -- Lab
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import execute_query, render_results_template, DATE, STRING, NUMBER
from indivo.models import Lab

LAB_FILTERS = {
  'lab_type': ('lab_type', STRING),
  'date_measured': ('date_measured', DATE),
  'lab_test_name': ('first_lab_test_name', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

LAB_TEMPLATE = 'reports/lab.xml'

@marsloader(query_api_support=True)
def lab_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  try:
    results, trc, aggregate_p = execute_query(Lab, LAB_FILTERS, 
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
  
  return render_results_template(results, trc, aggregate_p, LAB_TEMPLATE,
                                 group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters)

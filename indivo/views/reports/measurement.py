"""
Indivo Views -- Measurements
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import execute_query, render_results_template, DATE, STRING, NUMBER
from indivo.models import Measurement
import copy

MEASUREMENT_FILTERS = {
  'lab_code' : ('type', STRING),
  'value' : ('value', NUMBER),
  'date_measured' : ('datetime', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

MEASUREMENT_TEMPLATE = 'reports/measurement.xml'

def measurement_list(*args, **kwargs):
  """ For 1:1 mapping of URLs to views: calls _measurement_list """
  return _measurement_list(*args, **kwargs)

def carenet_measurement_list(*args, **kwargs):
  """ For 1:1 mapping of URLs to views: calls _measurement_list """
  return _measurement_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _measurement_list(request, group_by, date_group, aggregate_by,
                      limit, offset, order_by,
                      status, date_range, filters,
                      lab_code, record=None, carenet=None):
  query_filters = copy.copy(filters)
  if lab_code:
    query_filters['lab_code'] = lab_code

  try:
    results, trc, aggregate_p = execute_query(Measurement, MEASUREMENT_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, query_filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

  return render_results_template(results, trc, aggregate_p, MEASUREMENT_TEMPLATE,
                                 group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters)

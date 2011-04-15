"""
Indivo Views -- Measurements
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.utils import render_template
from indivo.lib.query import execute_query, DATE, STRING, NUMBER
from indivo.models import Measurement

MEASUREMENT_FILTERS = {
  'lab_code' : ('type', STRING),
  'value' : ('value', NUMBER),
  'date_measured' : ('datetime', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

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
  if lab_code:
    filters['lab_code'] = lab_code

  try:
    results, trc, aggregate_p = execute_query(Measurement, MEASUREMENT_FILTERS,
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
    return render_template('reports/measurements', 
                           { 'measurements': results,
                             'record': record,
                             'trc' : trc,
                             'limit' : limit,
                             'offset' : offset,
                             'order_by' : order_by}, 
                           type="xml")

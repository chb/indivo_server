"""
Indivo Views -- Medication
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import execute_query, render_results_template, DATE, STRING, NUMBER
from indivo.models import Medication

MEDICATION_FILTERS = {
  'medication_name' : ('name', STRING),
  'medication_brand_name' : ('brand_name', STRING),
  'date_started': ('date_started', DATE),
  'date_stopped': ('date_stopped', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

MEDICATION_TEMPLATE = 'reports/medication.xml'

def medication_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _medication_list"""
  return _medication_list(*args, **kwargs)

def carenet_medication_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _medication_list"""
  return _medication_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _medication_list(request, group_by, date_group, aggregate_by,
                     limit, offset, order_by,
                     status, date_range, filters,
                     record=None, carenet=None):

  try:
    results, trc, aggregate_p = execute_query(Medication, MEDICATION_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

  return render_results_template(results, trc, aggregate_p, MEDICATION_TEMPLATE,
                                 group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters)

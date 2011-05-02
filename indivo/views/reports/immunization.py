"""
Indivo Views -- Immunizations
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import execute_query, render_results_template, DATE, STRING, NUMBER
from indivo.models import Immunization

IMMUNIZATION_FILTERS = {
  'vaccine_type' : ('vaccine_type', STRING),
  'date_administered': ('date_administered', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

IMMUNIZATION_TEMPLATE = 'reports/immunization.xml'

def immunization_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _immunization_list"""
  return _immunization_list(*args, **kwargs)

def carenet_immunization_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _immunization_list"""
  return _immunization_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _immunization_list(request, group_by, date_group, aggregate_by,
                       limit, offset, order_by,
                       status, date_range, filters,
                       record=None, carenet=None):

  try:
    results, trc, aggregate_p = execute_query(Immunization, IMMUNIZATION_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

  return render_results_template(results, trc, aggregate_p, IMMUNIZATION_TEMPLATE,
                                 group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters)

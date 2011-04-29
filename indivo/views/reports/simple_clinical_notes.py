"""
Indivo Views -- Simple Clinical Notes
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import execute_query, render_results_template, DATE, STRING, NUMBER
from indivo.models import SimpleClinicalNote

SIMPLE_CLINICAL_NOTE_FILTERS = {
  'specialty' : ('specialty', STRING),
  'provider_name' : ('provider_name', STRING),
  'date_of_visit': ('date_of_visit', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

SIMPLE_CLINICAL_NOTE_TEMPLATE = 'reports/simple_clinical_note.xml'

@marsloader(query_api_support=True)
def simple_clinical_notes_list(request, group_by, date_group, aggregate_by,
                              limit, offset, order_by,
                              status, date_range, filters,
                              record=None, carenet=None):
  
  try:
    results, trc, aggregate_p = execute_query(SimpleClinicalNote, SIMPLE_CLINICAL_NOTE_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

  return render_results_template(results, trc, aggregate_p, SIMPLE_CLINICAL_NOTE_TEMPLATE,
                                 group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters)

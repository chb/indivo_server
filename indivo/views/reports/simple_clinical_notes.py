"""
Indivo Views -- Simple Clinical Notes
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.utils import render_template
from indivo.lib.query import execute_query, DATE, STRING, NUMBER
from indivo.models import SimpleClinicalNote

SIMPLE_CLINICAL_NOTE_FILTERS = {
  'specialty' : ('specialty', STRING),
  'provider_name' : ('provider_name', STRING),
  'date_of_visit': ('date_of_visit', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

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


  if aggregate_p:
    # Waiting on aggregate schema
    return HttpResponse(str(results))

  else:
    return render_template('reports/simple_clinical_notes', 
                           { 'scns' : results,
                             'trc' : trc,
                             'limit' : limit,
                             'offset' : offset,
                             'order_by' : order_by}, 
                           type="xml")

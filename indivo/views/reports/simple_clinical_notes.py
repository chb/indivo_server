"""
.. module:: views.reports.simple_clinical_notes
   :synopsis: Indivo view implementations for the simple_clinical_notes report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""


from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import SimpleClinicalNote

SIMPLE_CLINICAL_NOTE_FILTERS = {
  'specialty' : ('specialty', STRING),
  'provider_name' : ('provider_name', STRING),
  'date_of_visit': ('date_of_visit', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

SIMPLE_CLINICAL_NOTE_TEMPLATE = 'reports/simple_clinical_note.xml'

def simple_clinical_notes_list(*args, **kwargs):
  """ List the simple_clinical_notes data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.simple_clinical_notes._simple_clinical_notes_list`.

  """

  return _simple_clinical_notes_list(*args, **kwargs)

def carenet_simple_clinical_notes_list(*args, **kwargs):
  """ List the simple_clinical_notes data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.simple_clinical_notes._simple_clinical_notes_list`.

  """

  return _simple_clinical_notes_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _simple_clinical_notes_list(request, query_options,
                              record=None, carenet=None):
  """ List the simple_clinical_notes objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of simple clinical notes on 
  success, :http:statuscode:`400` if any invalid query parameters were passed.

  """  
  
  q = FactQuery(SimpleClinicalNote, SIMPLE_CLINICAL_NOTE_FILTERS,
                query_options,
                record, carenet)
  try:
    return q.render(SIMPLE_CLINICAL_NOTE_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

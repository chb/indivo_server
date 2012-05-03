"""
.. module:: views.reports.medication
   :synopsis: Indivo view implementations for the medication report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Medication, StatusName
from .generic import _generic_list

MEDICATION_FILTERS = {
  'medication_name' : ('name', STRING),
  'medication_brand_name' : ('brand_name', STRING),
  'date_started': ('date_started', DATE),
  'date_stopped': ('date_stopped', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

MEDICATION_TEMPLATE = 'reports/medication.xml'

def smart_medications(request, record):
  """ SMART-compatible alias for the generic list view on Medications, serialized as RDF. """

  default_query_args = {
    'limit': 100,
    'offset': 0,
    'order_by': '-%s'%DEFAULT_ORDERBY,
    'status': StatusName.objects.get(name='active'),
    'group_by': None,
    'aggregate_by': None,
    'date_range': None,
    'date_group': None,
    'filters': {},
    }
  return _generic_list(request, default_query_args, 'Medication', response_format="application/rdf+xml", record=record)


def medication_list(*args, **kwargs):
  """ List the medication data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.medication._medication_list`.

  """

  return _medication_list(*args, **kwargs)

def carenet_medication_list(*args, **kwargs):
  """ List the medication data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.medication._medication_list`.

  """

  return _medication_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _medication_list(request, query_options,
                     record=None, carenet=None):
  """ List the medication objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of medications on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Medication, MEDICATION_FILTERS,
                query_options,
                record, carenet)
  try:
    return q.render(MEDICATION_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

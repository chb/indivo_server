"""
.. module:: views.reports.allergy
   :synopsis: Indivo view implementations for the allergy report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.lib.rdf import PatientGraph
from indivo.models import Allergy, AllergyExclusion, StatusName

ALLERGY_FILTERS = {
  'date_diagnosed' : ('date_diagnosed', DATE),
  'allergen_type' : ('allergen_type', STRING),
  'allergen_name' : ('allergen_name', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

ALLERGY_TEMPLATE = 'reports/allergy.xml'

def smart_allergies(request, record):
  """ SMART allergy list, serialized as RDF.

  A bit more complicated than the generic list view, since we have to serialize AllergyExclusions as well.

  """

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
  allergies_query = FactQuery(Allergy, Allergy.filter_fields, default_query_args, record, None)
  exclusions_query = FactQuery(AllergyExclusion, AllergyExclusion.filter_fields, default_query_args, record, None)

  try:
    allergies_query.execute()
    exclusions_query.execute()
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

  graph = PatientGraph(record)
  graph.addAllergyList(allergies_query.results.iterator())
  graph.addAllergyExclusions(exclusions_query.results.iterator())
  return HttpResponse(graph.toRDF(), mimetype='application/rdf+xml')

def allergy_list(*args, **kwargs):
  """ List the allergy data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.allergy._allergy_list`.

  """

  return _allergy_list(*args, **kwargs)

def carenet_allergy_list(*args, **kwargs):
  """ List the allergy data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.allergy._allergy_list`.

  """

  return _allergy_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _allergy_list(request, query_options,
                       record=None, carenet=None):
  """ List the allergy objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of allergies on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Allergy, ALLERGY_FILTERS,
               query_options,
               record, carenet)
  try:
    return q.render(ALLERGY_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

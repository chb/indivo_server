"""
.. module:: views.reports.allergy
   :synopsis: Indivo view implementations for the allergy report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery
from indivo.lib.rdf import PatientGraph
from indivo.models import Allergy, AllergyExclusion, StatusName

def smart_allergies(request, record):
  """ SMART allergy list, serialized as RDF/XML.

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

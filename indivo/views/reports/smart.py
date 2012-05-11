"""
.. module:: views.reports.smart
   :synopsis: Indivo view implementations for SMART reports.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import DEFAULT_ORDERBY
from indivo.lib.query import FactQuery
from indivo.lib.rdf import PatientGraph
from indivo.models import StatusName, Allergy, AllergyExclusion
from .generic import _generic_list

SMART_URLS_TO_DATAMODELS = {
    'problems': 'Problem',
    'encounters': 'Encounter',
    'allergies': 'Allergy',
    'fulfillments': 'Fill', 
    'immunizations': 'Immunization',
    'lab_results': 'Lab',
    'medications': 'Medication',
    'vital_signs': 'Vitals',
}

def get_default_query_args():
    return {
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

def smart_generic(request, record, model_name):
    """ SMART-compatible alias for the generic list view: returns data_models serialized as SMART RDF."""

    default_query_args = get_default_query_args()
    data_model_name = SMART_URLS_TO_DATAMODELS.get(model_name, None)
    if not data_model_name:
        return HttpResponseBadRequest('Invalid SMART datamodel: %s'%model_name)
    return _generic_list(request, default_query_args, data_model_name, response_format="application/rdf+xml", record=record)

def smart_allergies(request, record):
  """ SMART allergy list, serialized as RDF/XML.

  A bit more complicated than the generic list view, since we have to serialize AllergyExclusions as well.

  """

  default_query_args = get_default_query_args()  
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


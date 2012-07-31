"""
.. module:: views.reports.smart
   :synopsis: Indivo view implementations for SMART reports.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

from django.http import HttpResponseBadRequest, HttpResponse, Http404, HttpResponseServerError
from django.db.models.loading import get_model
from indivo.lib.view_decorators import DEFAULT_ORDERBY
from indivo.lib.query import FactQuery
from indivo.lib.rdf import PatientGraph
from indivo.models import StatusName, Allergy, AllergyExclusion
from .generic import _generic_list
from django.shortcuts import render_to_response
from symbol import except_clause

SMART_URLS_TO_DATAMODELS = {
    'problems': 'Problem',
    'encounters': 'Encounter',
    'allergies': 'Allergy',
    'fulfillments': 'Fill', 
    'immunizations': 'Immunization',
    'lab_results': 'LabResult',
    'medications': 'Medication',
    'vital_signs': 'VitalSigns',
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
        raise Http404
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

def smart_generic_instance(request, record, model_name, model_id):
    """Retrieve a specific instance of a SMART model."""
    data_model_name = SMART_URLS_TO_DATAMODELS.get(model_name, None)
    if not data_model_name:
        # model mapping not found
        raise Http404
    model_class = get_model('indivo', data_model_name)
    if model_class is None:
        # model class not found
        raise Http404
    try:
        # we use .filter here instead of .get_object_or_404 so we have a QuerySet 
        # for serialization
        model_instance = model_class.objects.filter(id=model_id)
        if model_instance.count() == 1:
            # found
            data = model_class.to_rdf(model_instance, 1, record)
            return HttpResponse(data, mimetype='application/rdf+xml')
        elif model_instance.count() > 1:
            # more than a single instance found
            return HttpResponseServerError()
        else:
            # not found
            raise Http404
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    
def smart_allergies_instance(request, record, model_id):
    """Retrieve a specific instance of a SMART allergy.
    
    SMART allergies can be an Allergy or an AllergyExclusion
    
    """
    try:
        # Allergy and AllergyExclusion IDs are non-overlapping, so we can search
        # for them sequentially
        instance = Allergy.objects.filter(id=model_id)
        if instance.count() == 1:
            data = Allergy.to_rdf(instance, 1, record)
        else:
            instance = AllergyExclusion.objects.filter(id=model_id)
            if instance.count() == 1:
                data = AllergyExclusion.to_rdf(instance, 1, record)
            else:
                raise Http404
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    
    return HttpResponse(data, mimetype='application/rdf+xml')

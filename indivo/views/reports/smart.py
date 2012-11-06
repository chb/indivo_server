"""
.. module:: views.reports.smart
   :synopsis: Indivo view implementations for SMART reports.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

from django.http import HttpResponseBadRequest, HttpResponse, Http404, HttpResponseServerError
from django.db.models.loading import get_model
from indivo.lib.view_decorators import marsloader
from indivo.lib.query import FactQuery
from indivo.lib.rdf import PatientGraph
from indivo.models import Allergy, AllergyExclusion

from .generic import _generic_list

SMART_URLS_TO_DATAMODELS = {
    'problems': 'Problem',
    'encounters': 'Encounter',
    'allergies': 'Allergy',
    'fulfillments': 'Fill', 
    'immunizations': 'Immunization',
    'lab_results': 'LabResult',
    'medications': 'Medication',
    'vital_sign_sets': 'VitalSigns',
    'procedures': 'Procedure',
    'social_history': 'SocialHistory',
    'clinical_notes': 'ClinicalNote',
}

# used to transform SMART query filter fields to internal data model fields
SMART_QUERY_FILTERS = {
    'lab_results': {'loinc':'name_code_identifier'},
    'vital_sign_sets': {'encounter_type':'encounter_type_code_title'},
}

# defines what field SMART date filters apply to
SMART_DATE_FILTERS = {
    'lab_results':'date',
    'vital_sign_sets':'date',
}

@marsloader(query_api_support=True)
def smart_generic(request, query_options, record, model_name):
    """ SMART-compatible alias for the generic list view: returns data_models serialized as SMART RDF."""
    
    data_model_name = SMART_URLS_TO_DATAMODELS.get(model_name, None)
    if not data_model_name:
        raise Http404
    
    # replace filter fields based off mappings from SMART fields to data model fields
    # e.g. loinc => lab_name_code_identifier for LabResult
    field_mappings = SMART_QUERY_FILTERS.get(model_name)
    query_filters = query_options.get('filters') 
    if query_filters and field_mappings:
        for filter_key in query_filters:
            if field_mappings.has_key(filter_key):
                # found a filter we need to rename
                query_filters.update({field_mappings.get(filter_key):query_filters.pop(filter_key)})
                
    # transform SMART date query filters to Indivo filters
    if SMART_DATE_FILTERS.has_key(model_name):
        date_from = query_options.pop('date_from', None) #TODO iso8601 these, or is that handled in the query?
        date_to = query_options.pop('date_to', None)
        if date_from or date_to:
            date_range = {'field': SMART_DATE_FILTERS.get(model_name),
                          'start_date': date_from,
                          'end_date': date_to,
                          }
            # these options overwrite any date_range value passed to the query, since it is a SMART call
            query_options.update({'date_range':date_range})
            
    
    return _generic_list(request, query_options, data_model_name, response_format="application/rdf+xml", record=record)

@marsloader(query_api_support=True)
def smart_allergies(request, query_options, record):
    """ SMART allergy list, serialized as RDF/XML.
    
    A bit more complicated than the generic list view, since we have to serialize AllergyExclusions as well.
    
    """

    allergies_query = FactQuery(Allergy, Allergy.filter_fields, query_options, record, None)
    exclusions_query = FactQuery(AllergyExclusion, AllergyExclusion.filter_fields, query_options, record, None)
    
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

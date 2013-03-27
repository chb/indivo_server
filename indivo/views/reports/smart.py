"""
.. module:: views.reports.smart
   :synopsis: Indivo view implementations for SMART reports.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""
from itertools import chain
from operator import attrgetter
from django.http import HttpResponseBadRequest, HttpResponse, Http404, HttpResponseServerError
from django.db.models.loading import get_model
from indivo.lib.view_decorators import marsloader
from indivo.lib.query import FactQuery
from indivo.rdf.rdf import PatientGraph
from indivo.models import Allergy, AllergyExclusion

from .generic import _generic_list

SMART_URLS_TO_DATAMODELS = {
    'problems': 'Problem',
    'encounters': 'Encounter',
    'allergies': 'Allergy',
    'fulfillments': 'Fill', 
    'immunizations': 'Immunization',
    'lab_results': 'LabResult',
    'lab_panels': 'LabPanel',
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
        date_from = query_options.pop('date_from', None) 
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
    
    # Since SMART allergies queries span both data models, we need to get all 
    # results and then sort and limit after the fact to provide a reproducible
    # ordering
    options_resets = {'limit':None,
                      'offset':0,
                      }
    saved_limit = query_options.get('limit')
    saved_offset = query_options.get('offset')
    query_options.update(options_resets)
    # there should always be a default order_by
    order_by = query_options.get('order_by')
    descending_sort = order_by[0] == '-'
    order_by_field = order_by if not descending_sort else order_by[1:]
    
    # grab Allergies and Exclusions without limit or offset
    allergies_query = FactQuery(Allergy, Allergy().filter_fields, query_options, record, request_url=request.build_absolute_uri())
    exclusions_query = FactQuery(AllergyExclusion, AllergyExclusion().filter_fields, query_options, record, request_url=request.build_absolute_uri())
    
    try:
        allergies_query.execute()
        exclusions_query.execute()
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    # merge, sort and then apply offset/limit
    merged_results = sorted(
        chain(allergies_query.results, exclusions_query.results),
        key=attrgetter(order_by_field)
    )
    # limit and offset as needed
    if saved_limit:
        merged_results = merged_results[saved_offset:saved_offset+saved_limit]
    
    # mock up a "merged" query object
    allergies_query.results = merged_results
    allergies_query.trc = allergies_query.trc + exclusions_query.trc
    allergies_query.limit = saved_limit
    allergies_query.offset = saved_offset
    
    graph = PatientGraph(record)
    result_order = graph.addCombinedAllergyList(merged_results, True if saved_limit else False)
    graph.addCombinedResponseSummary(allergies_query, result_order)
    
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
        fact_query = FactQuery(model_class, model_class().filter_fields, {}, record, fact_id=model_id)
        fact_query.execute()
        if fact_query.trc == 1:
            # found
            data = model_class.to_rdf(fact_query, record)
            return HttpResponse(data, mimetype='application/rdf+xml')
        elif fact_query.trc > 1:
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
        fact_query = FactQuery(Allergy, Allergy().filter_fields, {}, record, None, model_id)
        fact_query.execute()
        if fact_query.trc == 1:
            data = Allergy.to_rdf(fact_query, record)
        else:
            fact_query = FactQuery(AllergyExclusion, AllergyExclusion().filter_fields, {}, record, None, model_id)
            fact_query.execute()
            if fact_query.trc == 1:
                data = AllergyExclusion.to_rdf(fact_query, record)
            else:
                raise Http404
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    
    return HttpResponse(data, mimetype='application/rdf+xml')

"""
.. module:: views.reports.generic
   :synopsis: Indivo view implementations for generic reports over any Model

.. moduleauthor:: Travers Franckle <travers.franckle@childrens.harvard.edu>

"""
from lxml import etree

from django.db.models.loading import get_model
from django.http import HttpResponseBadRequest, HttpResponse, Http404
from django.utils import simplejson

from indivo.lib.query import FactQuery
from indivo.lib.view_decorators import marsloader
from indivo.serializers.json import IndivoJSONEncoder

# map request content types to Model serialization types
SERIALIZATION_FORMAT_MAP = {
    'application/json': 'json',
    'application/xml': 'xml',
    'text/xml': 'xml',
    'application/rdf+xml': 'rdf',
}

def serialize(cls, format, query, record=None, carenet=None):
    """Serialize an indivo.lib.query to the requested format 
    
    Non-aggregate queries are handled by the data model's own serialization
    methods, while aggregate queries are serialized in a standard way to 
    AggregateReports
        
    **Returns:**
    
    * A string representation of the serialized query results in the requested 
      format
    
    """
     
    # aggregate queries
    if query.aggregate_by:
        return serialize_as_aggregate(format, query)
    
    # non-aggregate queries
    queryset = query.results
    result_count = query.trc
    method = "to_" + SERIALIZATION_FORMAT_MAP[format]
    if hasattr(cls, method):
        return getattr(cls, method)(queryset, result_count, record, carenet)
    else:
        raise ValueError("format not supported")

def serialize_as_aggregate(format, query):
    """Serialize an aggregate query to the requested format"""
    
    serialization_type = SERIALIZATION_FORMAT_MAP[format]
    results = None
    if serialization_type == 'xml':
        results = aggregate_xml(query)
    elif serialization_type == 'json':
        results = aggregate_json(query)
    else:
        raise ValueError("format not supported")
    
    return results

def aggregate_json(query):
    """Serialize an aggregate query's results to a JSON string"""
    
    results = []
    group_key = (query.group_by if query.group_by else query.date_group['time_incr']) 
    for row in query.results:
        row['__modelname__'] = 'AggregateReport'
        
        # rename the group key to 'group'
        row['group'] = row[group_key]
        del row[group_key]
        
        # rename 'aggregate_value' to 'value'
        row['value'] = row['aggregate_value']
        del row['aggregate_value']
        
        results.append(row)
        
    return simplejson.dumps(results, cls=IndivoJSONEncoder)
    
def aggregate_xml(query):
    """Serialize an aggregate query's results to an XML string"""
    
    root = etree.Element("AggregateReports")
    group_key = (query.group_by if query.group_by else query.date_group['time_incr']) 
    for row in query.results:
        row_element = etree.Element("AggregateReport", 
                                    value = str(row['aggregate_value']),
                                    group = row[group_key])
        root.append(row_element)
        
    return etree.tostring(root)

@marsloader(query_api_support=True)
def generic_list(request, query_options, data_model, record=None, carenet=None, response_format=None):
  """ List the Model data for a given record.

  """

  return _generic_list(request, query_options, data_model, record, carenet, response_format)

@marsloader(query_api_support=True)
def carenet_generic_list(request, query_options, data_model, record=None, carenet=None, response_format=None):
  """ List the Model data for a given carenet.

  """

  return _generic_list(request, query_options, data_model, record, carenet, response_format)


def _generic_list(request, query_options, data_model, record=None, carenet=None, response_format=None):
  """ List the Model objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of Models or AggregateReports 
  on success, :http:statuscode:`400` if any invalid query parameters were passed.

  """
  # check requested format
  if not response_format:
      response_format = request.GET.get("response_format", 'application/json')
  
  if not SERIALIZATION_FORMAT_MAP.has_key(response_format):
      # unsupported format
      return HttpResponseBadRequest("format not supported")
  
  # look up model
  model_class = get_model('indivo', data_model)
  if model_class is None:
      # model not found
      raise Http404

  # build query
  model_filters =  model_class.filter_fields # TODO: possible to make a lazy class property?
  query = FactQuery(model_class, 
                model_filters,
                query_options,
                record, 
                carenet)
  try:
      query.execute()
      data = serialize(model_class, response_format, query, record, carenet)
      return HttpResponse(data, mimetype=response_format)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

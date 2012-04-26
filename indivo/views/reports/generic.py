"""
.. module:: views.reports.generic
   :synopsis: Indivo view implementations for generic reports over any Model

.. moduleauthor:: Travers Franckle <travers.franckle@childrens.harvard.edu>

"""
from django.db.models.loading import get_model
from django.http import HttpResponseBadRequest, HttpResponse, Http404

from indivo.lib.query import FactQuery
from indivo.lib.view_decorators import marsloader

# map request content types to Model serialization methods
SERIALIZATION_FORMAT_MAP = {
    'application/json': 'to_json',
    'application/xml': 'to_xml',
    'text/xml': 'to_xml',
    'application/rdf+xml': 'to_rdf',
}

# serialize queryset to the requested format
def serialize(cls, format, queryset):
    method = SERIALIZATION_FORMAT_MAP[format]
    if hasattr(cls, method):
        return getattr(cls, method)(queryset)
    else:
        return HttpResponseBadRequest("format not supported")

def generic_list(*args, **kwargs):
  """ List the Model data for a given record.

  """

  return _generic_list(*args, **kwargs)

def carenet_generic_list(*args, **kwargs):
  """ List the Model data for a given carenet.

  """

  return _generic_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _generic_list(request, query_options, data_model,
              record=None, carenet=None):
  """ List the Model objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of Models on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """
  # check requested format
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
  q = FactQuery(model_class, 
                model_filters,
                query_options,
                record, 
                carenet)
  try:
      q.execute()
      data = serialize(model_class, response_format, q.results)
      return HttpResponse(data, mimetype=response_format)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

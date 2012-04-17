"""
.. module:: views.reports.simple_data_model
   :synopsis: Indivo view implementations for Simple Data Model reports

.. moduleauthor:: Travers Franckle <travers.franckle@childrens.harvard.edu>

"""
from django.core import serializers
from django.db.models.loading import get_model
from django.http import HttpResponseBadRequest, HttpResponse, Http404
from django.utils import simplejson

from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.serializers.json import IndivoJSONEncoder

def format_as_json(data):
    data = serializers.serialize("indivo_python", data)
    return simplejson.dumps(data, cls=IndivoJSONEncoder)

def format_as_xml(data):
    return serializers.serialize("indivo_xml", data)

RESPONSE_FORMAT_MAP = {
    'application/json': format_as_json,
    'application/xml': format_as_xml
}

def simple_data_model_list(*args, **kwargs):
  """ List the lab data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.lab._lab_list`.

  """

  return _simple_data_model_list(*args, **kwargs)

def carenet_simple_data_model_list(*args, **kwargs):
  """ List the lab data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.lab._lab_list`.

  """

  return _simple_data_model_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _simple_data_model_list(request, query_options, model_name,
              record=None, carenet=None):
  """ List the lab objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of labs on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """
  # check requested format
  response_format = request.GET.get("response_format", 'application/json')
  if not RESPONSE_FORMAT_MAP.has_key(response_format):
      # unsupported format
      return HttpResponseBadRequest("format not supported")
  
  # look up model
  model_class = get_model('indivo', model_name)
  if model_class is None:
      # model not found
      raise Http404

  # build query
  model_filters =  {DEFAULT_ORDERBY : ('created_at', DATE)} #TODO: need to implement: model_class.filter_fields 
  q = FactQuery(model_class, 
                model_filters,
                query_options,
                record, 
                carenet)
  try:
      q.execute()
      data = RESPONSE_FORMAT_MAP[response_format](q.results)
      return HttpResponse(data, mimetype=response_format)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

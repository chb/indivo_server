"""
Indivo Views -- Allergy
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Allergy

ALLERGY_FILTERS = {
  'date_diagnosed' : ('date_diagnosed', DATE),
  'allergen_type' : ('allergen_type', STRING),
  'allergen_name' : ('allergen_name', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

ALLERGY_TEMPLATE = 'reports/allergy.xml'

def allergy_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _allergy_list"""
  return _allergy_list(*args, **kwargs)

def carenet_allergy_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _allergy_list"""
  return _allergy_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _allergy_list(request, group_by, date_group, aggregate_by,
                       limit, offset, order_by,
                       status, date_range, filters,
                       record=None, carenet=None):
  q = FactQuery(Allergy, ALLERGY_FILTERS,
               group_by, date_group, aggregate_by,
               limit, offset, order_by,
               status, date_range, filters,
               record, carenet)
  try:
    return q.render(ALLERGY_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

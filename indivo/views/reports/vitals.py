"""
Indivo Views -- Vitals
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Vitals

VITALS_FILTERS = {
  'category' : ('name', STRING),
  'value' : ('value', NUMBER),
  'date_measured': ('date_measured', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

VITALS_TEMPLATE = 'reports/vital.xml'

def vitals_list(*args, **kwargs):
  """For 1:1 mapping from URLs to views: calls _vitals_list"""
  return _vitals_list(*args, **kwargs)

def carenet_vitals_list(*args, **kwargs):
  """For 1:1 mapping from URLs to views: calls _vitals_list"""
  return _vitals_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _vitals_list(request, group_by, date_group, aggregate_by,
                 limit, offset, order_by,
                 status, date_range, filters,
                 category=None, record=None, carenet=None):

  # change underscores to spaces in the category, to make it easier without URL encoding
  if category and not filters.has_key('category'):
    category = category.replace("_"," ")
    filters['category'] = category
    
  q = FactQuery(Vitals, VITALS_FILTERS,
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)

  try:
    return q.render(VITALS_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

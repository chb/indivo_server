"""
.. module:: views.reports.problem
   :synopsis: Indivo view implementations for the problem report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Problem, StatusName
from .generic import _generic_list

PROBLEM_FILTERS = {
  'name_title' : ('name_title', STRING),
  'startDate': ('startDate', DATE),
  'endDate': ('endDate', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

PROBLEM_TEMPLATE = 'reports/problem.xml'

def smart_problems(request, record):
  """ SMART-compatible alias for the generic list view on Problems, serialized as RDF. """

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
  return _generic_list(request, default_query_args, 'Problem', response_format="application/rdf+xml", record=record)

def problem_list(*args, **kwargs):
  """ List the problem data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.problem._problem_list`.

  """

  return _problem_list(*args, **kwargs)

def carenet_problem_list(*args, **kwargs):
  """ List the problem data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.problem._problem_list`.

  """

  return _problem_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _problem_list(request, query_options,
                  record=None, carenet=None):
  """ List the problem objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of problems on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Problem, PROBLEM_FILTERS,
                query_options,
                record, carenet)
  try:
    return q.render(PROBLEM_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

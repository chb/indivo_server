"""
.. module:: views.reports.problem
   :synopsis: Indivo view implementations for the problem report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Problem

PROBLEM_FILTERS = {
  'problem_name' : ('name', STRING),
  'date_onset': ('date_onset', DATE),
  'date_resolution': ('date_resolution', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

PROBLEM_TEMPLATE = 'reports/problem.xml'

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
def _problem_list(request, group_by, date_group, aggregate_by,
                  limit, offset, order_by,
                  status, date_range, filters,
                  record=None, carenet=None):
  """ List the problem objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of problems on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Problem, PROBLEM_FILTERS,
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(PROBLEM_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

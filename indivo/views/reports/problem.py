"""
Indivo Views -- Problem
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import execute_query, render_results_template, DATE, STRING, NUMBER
from indivo.models import Problem

PROBLEM_FILTERS = {
  'problem_name' : ('name', STRING),
  'date_onset': ('date_onset', DATE),
  'date_resolution': ('date_resolution', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

PROBLEM_TEMPLATE = 'reports/problem.xml'

def problem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _problem_list"""
  return _problem_list(*args, **kwargs)

def carenet_problem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views: calls _problem_list"""
  return _problem_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _problem_list(request, group_by, date_group, aggregate_by,
                  limit, offset, order_by,
                  status, date_range, filters,
                  record=None, carenet=None):

  try:
    results, trc, aggregate_p = execute_query(Problem, PROBLEM_FILTERS,
                                              group_by, date_group, aggregate_by,
                                              limit, offset, order_by,
                                              status, date_range, filters,
                                              record, carenet)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

  return render_results_template(results, trc, aggregate_p, PROBLEM_TEMPLATE,
                                 group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters)

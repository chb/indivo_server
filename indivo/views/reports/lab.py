"""
.. module:: views.reports.lab
   :synopsis: Indivo view implementations for the lab report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Lab

LAB_FILTERS = {
  'lab_type': ('lab_type', STRING),
  'date_measured': ('date_measured', DATE),
  'lab_test_name': ('first_lab_test_name', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

LAB_TEMPLATE = 'reports/lab.xml'

def lab_list(*args, **kwargs):
  """ List the lab data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.lab._lab_list`.

  """

  return _lab_list(*args, **kwargs)

def carenet_lab_list(*args, **kwargs):
  """ List the lab data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.lab._lab_list`.

  """

  return _lab_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _lab_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  """ List the lab objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of labs on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Lab, LAB_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(LAB_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

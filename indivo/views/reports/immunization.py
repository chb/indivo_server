"""
.. module:: views.reports.immunization
   :synopsis: Indivo view implementations for the immunization report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Immunization

IMMUNIZATION_FILTERS = {
  'vaccine_type' : ('vaccine_type', STRING),
  'date_administered': ('date_administered', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

IMMUNIZATION_TEMPLATE = 'reports/immunization.xml'

def immunization_list(*args, **kwargs):
  """ List the immunization data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.immunization._immunization_list`.

  """

  return _immunization_list(*args, **kwargs)

def carenet_immunization_list(*args, **kwargs):
  """ List the immunization data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.immunization._immunization_list`.

  """

  return _immunization_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _immunization_list(request, group_by, date_group, aggregate_by,
                       limit, offset, order_by,
                       status, date_range, filters,
                       record=None, carenet=None):
  """ List the immunization objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of immunizations on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Immunization, IMMUNIZATION_FILTERS,
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(IMMUNIZATION_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

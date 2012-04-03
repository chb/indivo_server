"""
.. module:: views.reports.procedure
   :synopsis: Indivo view implementations for the procedure report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Procedure

PROCEDURE_FILTERS = {
  'procedure_name' : ('name', STRING),
  'date_performed': ('date_performed', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

PROCEDURE_TEMPLATE = 'reports/procedure.xml'

def procedure_list(*args, **kwargs):
  """ List the procedure data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.procedure._procedure_list`.

  """

  return _procedure_list(*args, **kwargs)

def carenet_procedure_list(*args, **kwargs):
  """ List the procedure data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.procedure._procedure_list`.

  """
  
  return _procedure_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _procedure_list(request, query_options,
                    record=None, carenet=None):
  """ List the procedure objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of procedures on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Procedure, PROCEDURE_FILTERS,
                query_options,
                record, carenet)

  try:
    return q.render(PROCEDURE_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))

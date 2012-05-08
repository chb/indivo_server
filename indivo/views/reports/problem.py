"""
.. module:: views.reports.problem
   :synopsis: Indivo view implementations for the problem report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.lib.view_decorators import DEFAULT_ORDERBY
from indivo.models import StatusName
from .generic import _generic_list

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

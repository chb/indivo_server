"""
.. module:: views.reports.encounter
   :synopsis: Indivo view implementations for the encounter report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Travers Franckle <travers.franckle@childrens.harvard.edu>

"""

from indivo.lib.view_decorators import DEFAULT_ORDERBY
from indivo.models import StatusName
from .generic import _generic_list

def smart_encounters(request, record):
  """ SMART-compatible alias for the generic list view on Encounters, serialized as RDF. """

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

  return _generic_list(request, default_query_args, 'Encounter', response_format="application/rdf+xml", record=record)

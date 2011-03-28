"""
Indivo Views -- Immunizations
"""

from django.http import HttpResponseBadRequest
from indivo.lib.view_decorators import marsloader
from indivo.lib.utils import render_template, carenet_filter
from indivo.models import *
from reportutils import report_orderby_update


@marsloader
def immunization_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  """For 1:1 mapping of URLs to views: calls _immunization_list"""
  return _immunization_list(request, limit, offset, status, order_by, record, carenet)


@marsloader
def carenet_immunization_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  """For 1:1 mapping of URLs to views: calls _immunization_list"""
  return _immunization_list(request, limit, offset, status, order_by, record, carenet)

def _immunization_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  if carenet:
    record = carenet.record
  if not record:
    return HttpResponseBadRequest()

  processed_order_by = report_orderby_update(order_by)

  immunizations = carenet_filter(carenet, 
                    Immunization.objects.select_related().filter(
                      record=record, 
                      document__status=status).order_by(processed_order_by))
  return render_template('reports/immunizations', 
                          { 'immunizations' : immunizations[offset:offset+limit], 
                            'trc' : len(immunizations),
                            'limit' : limit,
                            'offset' : offset,
                            'order_by' : order_by}, 
                            type="xml")

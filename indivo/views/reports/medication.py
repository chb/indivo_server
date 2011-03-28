"""
Indivo Views -- Medication
"""

from django.http import HttpResponseBadRequest
from indivo.lib.view_decorators import *
from indivo.lib.utils import render_template, carenet_filter
from indivo.models import *
from reportutils import report_orderby_update


@marsloader
def medication_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  """For 1:1 mapping of URLs to views. Calls _medication_list"""
  return _medication_list(request, limit, offset, status, order_by, record, carenet)


@marsloader
def carenet_medication_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  """For 1:1 mapping of URLs to views. Calls _medication_list"""
  return _medication_list(request, limit, offset, status, order_by, record, carenet)

def _medication_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  if carenet:
    record = carenet.record
  if not record:
    return HttpResponseBadRequest()

  processed_order_by = report_orderby_update(order_by)

  medications = carenet_filter(carenet,
                  Medication.objects.select_related().filter(
                    record=record, 
                    document__status=status).order_by(processed_order_by))
  return render_template('reports/medications', 
                          { 'medications' : medications[offset:offset+limit],
                            'trc' : len(medications),
                            'limit' : limit,
                            'offset' : offset,
                            'order_by' : order_by
                          }, 
                          type="xml")

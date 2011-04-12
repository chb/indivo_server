"""
Indivo Views -- Allergy
"""

from django.http import HttpResponseBadRequest
from indivo.lib.view_decorators import marsloader
from indivo.lib.utils import render_template, carenet_filter
from indivo.models import *
from reportutils import report_orderby_update


@marsloader()
def allergy_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  """For 1:1 mapping of URLs to views. Calls _allergy_list"""
  return _allergy_list(request, limit, offset, status, order_by, record, carenet)


@marsloader()
def carenet_allergy_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  """For 1:1 mapping of URLs to views. Calls _allergy_list"""
  return _allergy_list(request, limit, offset, status, order_by, record, carenet)

def _allergy_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  if carenet:
    record = carenet.record
  if not record:
    return HttpResponseBadRequest()

  processed_order_by = report_orderby_update(order_by)

  allergies = carenet_filter(carenet,
                             Allergy.objects.select_related().filter(record=record,
                                                                     document__status=status).order_by(processed_order_by))

  return render_template('reports/allergies', 
                          { 'allergies' : allergies[offset:offset+limit], 
                            'trc' : len(allergies),
                            'limit' : limit,
                            'offset' : offset,
                            'order_by' : order_by }, 
                          type="xml")

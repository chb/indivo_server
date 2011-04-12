"""
Indivo Views -- Vitals
"""

from django.http import HttpResponseBadRequest
from indivo.lib.view_decorators import marsloader
from indivo.lib.utils import render_template, carenet_filter
from indivo.models import *
from reportutils import report_orderby_update


@marsloader()
def vitals_list(request, limit, offset, status, category=None, order_by='-created_at', record=None, carenet=None):
  """For 1:1 mapping from URLs to views: calls _vitals_list"""
  return _vitals_list(request, limit, offset, status, category, order_by, record, carenet)


@marsloader()
def carenet_vitals_list(request, limit, offset, status, category=None, order_by='-created_at', record=None, carenet=None):
  """For 1:1 mapping from URLs to views: calls _vitals_list"""
  return _vitals_list(request, limit, offset, status, category, order_by, record, carenet)

def _vitals_list(request, limit, offset, status, category=None, order_by='-created_at', record=None, carenet=None):
  if carenet:
    record = carenet.record
  if not record:
    return HttpResponseBadRequest()

  # change underscores to spaces in the category, to make it easier without URL encoding
  if category:
    category = category.replace("_"," ")

  processed_order_by = report_orderby_update(order_by)

  if category:
    vitals = carenet_filter(carenet,
              Vitals.objects.select_related().filter(
                record=record, 
                name=category, 
                document__status=status).order_by(processed_order_by))
  else:
    vitals = carenet_filter(carenet,
                Vitals.objects.select_related().filter(
                  record=record, 
                  document__status=status).order_by(processed_order_by))
  return render_template('reports/vitals', 
                          { 'vitals' : vitals[offset:offset+limit],
                            'trc' : len(vitals),
                            'limit' : limit,
                            'offset' : offset,
                            'order_by' : order_by
                          }, type='xml')

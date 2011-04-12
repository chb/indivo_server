"""
Indivo Views -- Simple Clinical Notes
"""

from django.http import HttpResponseBadRequest
from indivo.lib.view_decorators import marsloader
from indivo.lib.utils import render_template, carenet_filter
from indivo.models import *
from reportutils import report_orderby_update


@marsloader()
def simple_clinical_notes_list(request, limit, offset, status, order_by='created_at', record=None, carenet=None):
  if carenet:
    record = carenet.record
  if not record:
    return HttpResponseBadRequest()

  processed_order_by = report_orderby_update(order_by)

  simple_clinical_notes = carenet_filter(carenet,
                SimpleClinicalNote.objects.select_related().filter(
                  record=record, 
                  document__status=status).order_by(processed_order_by))
  return render_template('reports/simple_clinical_notes', 
                          { 'scns' : simple_clinical_notes[offset:offset+limit],
                            'trc' : len(simple_clinical_notes),
                            'limit' : limit,
                            'offset' : offset,
                            'order_by' : order_by
                          }, 
                          type='xml')

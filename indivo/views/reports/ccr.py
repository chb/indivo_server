"""
Indivo Report - CCR
"""

from django.http import HttpResponseBadRequest
from indivo.lib.view_decorators import marsloader
from indivo.lib.utils import render_template
from indivo.lib.sharing_utils import carenet_facts_filter
from indivo.models import *
from reportutils import report_orderby_update

import datetime


def report_ccr(request, record=None, carenet=None):
  if carenet:
    record = carenet.record
  if not record:
    return HttpResponseBadRequest()

  # FIXME: fix these carenet filters to be smarter

  active_status = StatusName.objects.get(name='active')

  medications = carenet_facts_filter(carenet,
                                     Medication.objects.select_related().filter(record=record, document__status=active_status))
  immunizations = carenet_facts_filter(carenet, 
                                       Immunization.objects.select_related().filter(record=record, 
                                                                                    document__status=active_status))
  vitalsigns = carenet_facts_filter(carenet,
                                    Vitals.objects.select_related().filter(record=record, 
                                                                           document__status=active_status))


  return render_template('reports/ccr', 
                         {'record': record, 'now': datetime.datetime.utcnow(),
                          'medications': medications,
                          'immunizations' : immunizations,
                          'vitalsigns' : vitalsigns},
                         type="xml")

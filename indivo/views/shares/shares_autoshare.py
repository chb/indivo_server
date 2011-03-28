"""
Indivo views -- Sharing
"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from indivo.document_processing.document_processing import DocumentProcessing

def carenet_nevershare(request, document_id):
  # Not Yet Implemented
  #CarenetNeverShare.objects.create(document=Document.objects.get(id=document_id))
  return Done


def autoshare_list(request, record):
  TYPE = 'type'
  autoshares = []
  if request.GET.has_key(TYPE):
    try:
      docschema = DocumentSchema.objects.get(type = DocumentProcessing.expand_schema(request.GET[TYPE]))
    except DocumentSchema.DoesNotExist:
      raise Http404
    carenets = [autoshare.carenet for autoshare in CarenetAutoshare.objects.select_related().filter(
                  record = record, type = docschema)]
  return render_template('carenets', {  'carenets'  : carenets, 
                                        'record'    : record}, type="xml")


def autoshare_list_bytype_all(request, record):
  """
  provide all of the autoshares, grouped by type
  """
  autoshares = CarenetAutoshare.objects.select_related().filter(record = record).order_by('type')

  # group them by type
  autoshares_by_type = {}
  
  for autoshare in autoshares:
    if not autoshares_by_type.has_key(autoshare.type):
      autoshares_by_type[autoshare.type] = []

    autoshares_by_type[autoshare.type].append(autoshare)

  return render_template('all_autoshares_bytype', {  'autoshares_by_type'  : autoshares_by_type, 
                                        'record'    : record}, type="xml")


def autoshare_create(request, record, carenet):
  TYPE = 'type'
  if request.POST.has_key(TYPE):
    try:
      docschema = DocumentSchema.objects.get(type = DocumentProcessing.expand_schema(request.POST[TYPE]))
    except DocumentSchema.DoesNotExist:
      raise Http404
    CarenetAutoshare.objects.create(record  = record, 
                                    carenet = carenet, 
                                    type    = docschema)
  return DONE


def autoshare_delete(request, record, carenet):
  TYPE = 'type'
  if request.POST.has_key(TYPE):
    try:
      docschema = DocumentSchema.objects.get(type = DocumentProcessing.expand_schema(request.POST[TYPE]))
    except DocumentSchema.DoesNotExist:
      raise Http404
    CarenetAutoshare.objects.filter(record  = record, 
                                    carenet = carenet,
                                    type    = docschema).delete()
  return DONE

def autoshare_revert(request, record, document_id, carenet):
  # Not yet implemented
  return DONE

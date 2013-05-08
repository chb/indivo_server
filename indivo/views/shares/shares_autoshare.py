"""
.. module:: views.sharing.shares_autoshare
   :synopsis: Indivo view implementations related to autoshares of documents.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

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
  """ For a single record, list all carenets that a given doctype is autoshared with.
  
  request.GET must contain:
  
  * *type*: the document schema namespace to check autoshares for

  Will return :http:statuscode:`200` with a list of carenets that have an autoshare
  set up for doctype *type* on success, :http:statuscode:`404`
  if the specified *type* doesn't exist, or :http:statuscode:`400` if no type specified

  """

  TYPE = 'type'
  autoshares = []
  if request.GET.has_key(TYPE):
    try:
      docschema = DocumentSchema.objects.get(type = DocumentProcessing.expand_schema(request.GET[TYPE]))
    except DocumentSchema.DoesNotExist:
      raise Http404
    carenets = [autoshare.carenet for autoshare in CarenetAutoshare.objects.select_related().filter(
                  record = record, type = docschema)]
  else:
      # no type specified
    return HttpResponseBadRequest('No type specified')

  return render_template('carenets', {  'carenets'  : carenets, 
                                        'record'    : record}, type="xml")


def autoshare_list_bytype_all(request, record):
  """ For a single record, list all doctypes autoshared into carenets.
  
  Will return :http:statuscode:`200` with a list of doctypes and the
  carenets that have an autoshare for each doctype on success.

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
  """ Automatically share all documents of a certain type into a carenet.
  
  request.POST must contain:
  
  * *type*: the document schema namespace to create an autoshare for

  Will return :http:statuscode:`200` on sucess, :http:statuscode:`404`
  if the specified *type* doesn't exist.

  """

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
  """ Remove an autoshare from a carenet.
  
  request.POST must contain:
  
  * *type*: the document schema namespace to remove an autoshare for

  This will effectively unshare all documents of type *type* from the carenet,
  except documents which were shared individually.

  Will return :http:statuscode:`200` on sucess, :http:statuscode:`404`
  if the specified *type* doesn't exist.

  """

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
  """ Revert the document-sharing of a document in a carent to whatever rules are specified by autoshares. NOT IMPLEMENTED."""
  # Not yet implemented
  return DONE

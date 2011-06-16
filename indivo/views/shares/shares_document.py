"""
Indivo views -- Sharing
"""

import indivo.views
from indivo.lib.sharing_utils import carenet_documents_filter, document_in_carenet, document_carenets_filter
from indivo.views.base import *
from indivo.views.documents.document import _render_documents, _get_document, _render_document
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied

from django.db.models import F
from indivo.models import Document

@transaction.commit_on_success
def carenet_document_placement(request, record, carenet, document_id):
  """
  Place a document into a given carenet
  """
  document = _get_document(document_id=document_id, record=record)

  # don't allow this for nevershare documents
  if not document or document.nevershare:
    raise Http404

  CarenetDocument.objects.get_or_create(carenet=carenet, document=document)
  return DONE


def carenet_document_delete(request, carenet, record, document_id):
  """Delete a document into a given carenet"""

  document = _get_document(document_id=document_id, record=record)

  # this is always permission denied, so we can just handle it here
  # not in the access control system
  if not document or document.record != carenet.record:
    raise Http404

  doc_share, created_p = CarenetDocument.objects.get_or_create(document = document, carenet = carenet, defaults={'share_p':False})

  if not created_p and doc_share.share_p:
    doc_share.share_p = False
    doc_share.save()

  return DONE


def carenet_record(request, carenet):
  """Basic record information within a carenet

  For now, just the record label
  """
  return render_template('record', {'record': carenet.record})


@marsloader()
def carenet_document_list(request, carenet, limit, offset, status, order_by):
  """List documents from a given carenet

    Return both documents in the given carenet and 
    documents with the same types as in the record's autoshare

  """
  
  try:
    doc_type_uri = request.GET.get('type', None)
    if doc_type_uri:
      requested_doc_type = DocumentSchema.objects.get(type = doc_type_uri)
    else:
      requested_doc_type = None
  except DocumentSchema.DoesNotExist:
    raise Http404

  documents = carenet_documents_filter(carenet, carenet.record.documents)
  tdc = documents.count()

  ret_documents = documents[offset:offset+limit]

  return _render_documents(ret_documents, carenet.record, None, tdc)



def carenet_document(request, carenet, document_id):
  """Return a document given a record and carenet id

    Return the document if it is in the given carenet or 
    its type is in the record's autoshare
  """
  
  document = _get_document(document_id=document_id, carenet=carenet)
  if not document or document.nevershare:
    raise Http404

  if document_in_carenet(carenet, document_id):
    return _render_document(document)
  else: 
    raise Http404

def document_carenets(request, record, document_id):
  """List all the carenets for a given document

    This view retrieves all the carenets in which  a given 
    document has been placed
  """
  document = _get_document(document_id=document_id, record=record)
  if not document:
    raise Http404

  # Get the carenets
  carenets = document_carenets_filter(document, Carenet.objects.all())

  return render_template('carenets', {'carenets' : carenets, 'record' : record})

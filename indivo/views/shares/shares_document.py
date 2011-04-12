"""
Indivo views -- Sharing
"""

import indivo.views
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
    doc_share.share_p = True
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

    FIXME: this needs refactoring so it's one query for the whole thing,
    rather than one query per auto-share doctype
  """
  
  try:
    doc_type_uri = request.GET.get('type', None)
    if doc_type_uri:
      requested_doc_type = DocumentSchema.objects.get(type = doc_type_uri)
    else:
      requested_doc_type = None
  except DocumentSchema.DoesNotExist:
    raise Http404

  # we want to select
  # the documents that are explicitly shared
  # plus the documents that are auto-shared
  # minus the documents that are explicitly un-shared
  
  record = carenet.record
  
  # documents explicitly shared
  explicitly_shared = record.documents.filter(carenetdocument__share_p = True, carenetdocument__carenet = carenet, nevershare= False)
  if requested_doc_type:
    explicitly_shared = explicitly_shared.filter(type = requested_doc_type)

  # auto-shared documents that are not in the negatively shared space
  autoshared_types = DocumentSchema.objects.filter(carenetautoshare__carenet = carenet).values('id')
  implicitly_shared = record.documents.filter(type__in = autoshared_types, nevershare=False).exclude(carenetdocument__share_p = False, carenetdocument__carenet = carenet)

  if requested_doc_type:
    implicitly_shared = implicitly_shared.filter(type = requested_doc_type)

  # FIXME: we should make this lazy so that it's not evaluated right now
  all_documents = [d for d in explicitly_shared] + [d for d in implicitly_shared]

  documents = all_documents[offset:offset+limit]

  return _render_documents(documents, record, None, len(documents))



def carenet_document(request, carenet, document_id):
  """Return a document given a record and carenet id

    Return the document if it is in the given carenet or 
    its type is in the record's autoshare
  """
  
  document = _get_document(document_id=document_id, carenet=carenet)
  if not document or document.nevershare:
    raise Http404

  try:
    if CarenetDocument.objects.filter(carenet = carenet, document = document, carenet__record = carenet.record, share_p=True) or \
          (CarenetAutoshare.objects.filter(carenet = carenet, record = carenet.record, type = document.type) and \
             not CarenetDocument.objects.filter(carenet = carenet, document = document, share_p=False)):
      return _render_document(document)
    else: 
      raise Http404
  except Carenet.DoesNotExist:
    raise Http404


def document_carenets(request, record, document_id):
  """List all the carenets for a given document

    This view retrieves all the carenets in which  a given 
    document has been placed
  """
  document = _get_document(document_id=document_id, record=record)
  if not document:
    raise Http404

  if document.nevershare:
    carenets = []
  else:
    # the carenets for which a carenetdocument share exists with that particular document
    carenets = Carenet.objects.filter(carenetdocument__document = document, carenetdocument__share_p=True)
    
  return render_template('carenets', {'carenets' : carenets, 'record' : record})

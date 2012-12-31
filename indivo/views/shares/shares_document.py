"""
.. module:: views.sharing.shares_document
   :synopsis: Indivo view implementations related to sharing documents

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

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
  """ Place a document into a given carenet.

  Will return :http:statuscode:`200` on success, :http:statuscode:`404` if
  *document_id* doesn't exist or if *document_id* has a nevershare set
  on it.

  """

  document = _get_document(document_id=document_id, record=record)

  # don't allow this for nevershare documents
  if not document or document.nevershare:
    raise Http404

  CarenetDocument.objects.get_or_create(carenet=carenet, document=document)
  return DONE


def carenet_document_delete(request, carenet, record, document_id):
  """ Unshare a document from a given carenet.

  If there is an autoshare of *document_id*'s type into *carenet*, this 
  call creates an exception for *document_id* in *carenet*. If *document_id*
  was shared individually into *carenet*, this call removes it. If *document_id*
  is not shared in *carenet* at all, this call does nothing immediately.
  
  In all cases, this call exempts *document_id* from any future autoshares into
  this carenet.

  Will return :http:statuscode:`200` on success, :http:statuscode:`404` if 
  *document_id* doesn't exist or if *document_id* or *carenet* don't belong
  to *record*.

  """

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
  """ Get basic information about the record to which a carenet belongs.

  For now, info is the record id, label, creation time, creator, contact,
  and demographics.

  Will return :http:statuscode:`200` with XML about the record on success.

  """
  return render_template('record', {'record': carenet.record})


@marsloader()
def carenet_document_list(request, carenet, query_options):
  """List documents from a given carenet.

  request.GET may contain:
  
  * *type*: The document schema type to filter on.

  Returns both documents in the given carenet and documents with the same types 
  as in the record's autoshare, filtered by *type* if passed.

  Will return :http:statuscode:`200` with a document list on success,
  :http:statuscode:`404` if *type* doesn't exist.

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

  offset = query_options['offset']
  limit = query_options['limit']
  if limit:
      documents = documents[offset:offset+limit]

  return _render_documents(documents, carenet.record, None, tdc)



def carenet_document(request, carenet, document_id):
  """Return a document from a carenet.

  Will only return the document if it exists within the carenet.
  
  Will return :http:statuscode:`200` with the document content on success,
  :http:statuscode:`404` if *document_id* is invalid or if the indicated
  document is not shared in *carenet*.

  """
  
  document = _get_document(document_id=document_id, carenet=carenet)
  if not document or document.nevershare:
    raise Http404

  if document_in_carenet(carenet, document_id):
    return _render_document(document)
  else: 
    raise Http404

def document_carenets(request, record, document_id):
  """List all the carenets into which a document has been shared.

  Will return :http:statuscode:`200` with a list of carenets on success,
  :http:statuscode:`404` if *document_id* is invalid.
  
  """
  document = _get_document(document_id=document_id, record=record)
  if not document:
    raise Http404

  # Get the carenets
  carenets = document_carenets_filter(document, Carenet.objects.all())

  return render_template('carenets', {'carenets' : carenets, 'record' : record})

from indivo.views.base import *
from indivo.views.documents.document import _get_document

def app_document_delete(request, pha, document_id):
  """
  Delete an application specific document: no restrictions, since this storage is 
  managed by the app.
  """
  document = _get_document(pha=pha, document_id=document_id)
  if not document:
    raise Http404

  document.delete()
  return DONE

def record_app_document_delete(request, record, pha, document_id):
  """
  Delete a record-application specific document: no restrictions, since this storage is 
  managed by the app.
  """
  document = _get_document(record=record, pha=pha, document_id=document_id)
  if not document:
    raise Http404

  document.delete()
  return DONE

def record_document_delete(request, document_id, record):
  """Delete a recently added document, only if it was recently added by the same person"""
  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  # FIXME: modularize timedelta(hours=1)
  # For now, 1 hour
  if document.creator == request.principal.effective_principal and \
      datetime.datetime.now() - document.created_at < datetime.timedelta(hours=1):

    # we mean explicitly for this to fail 
    # if the document is referenced by anything in the DB

    document.delete()
    return DONE
  else:
    return HttpResponseBadRequest("document was inserted too long ago to delete, or was not created by you")


def documents_delete(request, record):
  Document.objects.filter(record=record).delete()
  return DONE

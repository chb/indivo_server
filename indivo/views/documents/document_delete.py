from indivo.views.base import *
from indivo.views.documents.document import _get_document

def app_document_delete(request, pha, document_id):
  """
  Delete an application specific document: no restrictions, since this storage is 
  managed by the app.
  """
  return _document_delete(document_id, pha=pha)

def record_app_document_delete(request, record, pha, document_id):
  """
  Delete a record-application specific document: no restrictions, since this storage is 
  managed by the app.
  """
  return _document_delete(document_id, pha=pha, record=record)


def _document_delete(document_id, pha=None, record=None):
  """Delete a document"""
  document = _get_document(record=record, pha=pha, document_id=document_id)
  if not document:
    raise Http404

  document.delete()
  return DONE

def documents_delete(request, record):
  Document.objects.filter(record=record).delete()
  return DONE

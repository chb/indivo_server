from indivo.views.base import *
from indivo.views.documents.document import _get_document

def document_delete(request, document_id, record):
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
    raise Exception("document was inserted too long ago to allow this, or was not created by you")


def documents_delete(request, record):
  Document.objects.filter(record=record).delete()
  return DONE

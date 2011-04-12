from indivo.views.base import *
from indivo.views.documents.document import _document_create, _render_documents, _set_doc_latest, _get_document

@transaction.commit_on_success
def document_version(request, record, document_id):
  """Version a document without external_id: just calls _document_version"""
  return _document_version(request, record, document_id)

@transaction.commit_on_success
def document_version_by_ext_id(request, record, document_id, pha, external_id):
  """Version a document with an external_id: just calls _document_version"""
  return _document_version(request, record, document_id, pha=pha, external_id=external_id)

def _document_version(request, record, document_id, pha=None, external_id=None):
  """Version a document, *cannot* be a non-record document"""

  old_document = _get_document(record=record, document_id=document_id)
  if not old_document:
    raise Http404

  full_external_id = Document.prepare_external_id(external_id, pha)
  try:
    new_doc = _document_create(record=record, 
                               creator=request.principal, 
                               content=request.raw_post_data,
                               replaces_document = old_document, 
                               pha=None,
                               external_id = full_external_id,
                               mime_type=utils.get_content_type(request))
  except:
    raise Http404

  _set_doc_latest(new_doc)
  return render_template('document', {'record'  : record, 
                                      'doc'     : new_doc, 
                                      'pha'     : None })



@marsloader()
def document_versions(request, record, document_id, limit, offset, status, order_by='created_at'):
  """Retrieve the versions of a document"""
  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  try:
    docs = Document.objects.filter( original  = document.original_id, 
                                    status    = status).order_by(order_by)
  except:
    raise Http404
  return _render_documents(docs[offset:offset+limit], record, None, len(docs))

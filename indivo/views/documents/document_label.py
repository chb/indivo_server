from indivo.views.base import *
from indivo.views.documents.document import _render_documents, _get_document



def app_document_label(request, pha, document_id):
  """For a 1:1 mapping of URLs to views: calls document_label"""
  return _document_label(request, pha=pha, document_id=document_id, app_specific=True)


def record_app_document_label(request, record, pha, document_id):
  """For a 1:1 mapping of URLs to views: calls document_label"""
  return _document_label(request, record=record, pha=pha, document_id=document_id, app_specific=True)


def record_document_label(request, record, document_id):
  """For a 1:1 mapping of URLs to views: calls document_label"""
  return _document_label(request, record=record, document_id=document_id, app_specific=False)


def record_document_label_ext(request, record, document=None, external_id=None, pha=None, app_specific=False):
  """For a 1:1 mapping of URLs to views: calls document_label"""
  return _document_label(request, record, document, external_id, pha, app_specific)

def _document_label(request, record=None, document_id=None, external_id=None, pha=None, app_specific=False):
  """
  set the document label
  """
  label = request.raw_post_data

  # Get the document
  full_external_id = Document.prepare_external_id(external_id, pha, pha_specific = app_specific)
  if not app_specific:
    pha = None
  document = _get_document(record=record, document_id=document_id, pha=pha, external_id=full_external_id)
    
  if document:
    if pha and document.pha != pha:
      raise Http404

    if record and document.record != record:
      raise Http404
  else:
    raise Http404

  document.label = label
  document.save()

  return _render_documents([document], record, pha, 1)

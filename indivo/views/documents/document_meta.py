from indivo.views.base import *
from indivo.views.documents.document import _set_doc_latest, _get_doc_relations, _get_document


def update_document_meta(request, record, document_id):
  # Does Nothing
  return DONE


def carenet_document_meta(request, carenet, document_id):
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  document = _get_document(carenet=carenet, document_id=document_id)
  return _document_meta(carenet=carenet, document=document)


def record_document_meta(request, record, document_id):
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  document = _get_document(record=record, document_id=document_id)
  return _document_meta(record=record, document=document)


def record_document_meta_ext(request, record, pha, external_id):
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  return _document_meta(record=record, pha=pha, external_id=external_id)


def app_document_meta(request, pha, document_id):
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  document = _get_document(pha=pha, document_id=document_id)
  return _document_meta(pha=pha, document=document, app_specific=True)

def app_document_meta_ext(request, pha, external_id):
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  return _document_meta(pha=pha, external_id=external_id, app_specific=True)


def record_app_document_meta(request, record, pha, document_id):
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  document = _get_document(record=record, pha=pha, document_id=document_id)
  return _document_meta(record=record, document=document, pha=pha, app_specific=True)


def record_app_document_meta_ext(request, record, pha, external_id):
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  return _document_meta(record=record, pha=pha, external_id=external_id, app_specific=True)


def _document_meta(record=None, carenet=None, document=None, pha=None, external_id=None, app_specific=False):
  """
  The metadata for a single document
  """
  if carenet:
    record = carenet.record

  if not document:
    full_external_id = Document.prepare_external_id(external_id, pha=pha, 
                                                    pha_specific=app_specific, 
                                                    record_specific=(record is not None))
    if not full_external_id:
      raise Http404

    if not app_specific:
      pha = None
    document = _get_document(record=record, pha=pha, external_id=full_external_id)
    if not document:
      raise Http404

  _set_doc_latest(document)

  # related stuff
  document.relates_to, document.is_related_from = _get_doc_relations(document)

  return render_template('single_document', {'doc' : document, 'record': document.record})

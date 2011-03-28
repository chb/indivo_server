from indivo.views.base import *
from indivo.views.documents.document import _document_create, _render_documents, _get_document

@marsloader
def get_documents_by_rel(request, record, document_id, rel, limit, offset, status, order_by='id', pha=None):
  """
  get all documents related to argument-document by rel-type defined by rel
  includes relationships to other versions of the argument-document
  (also limit, offset and status)
  """
  # Need to add limit, offset, order_by
  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  tdc = 0
  try:
    relationship = DocumentSchema.objects.get(type=DocumentSchema.expand_rel(rel))
    docs = Document.objects.filter(record=record,
                                   status=status,
                                   rels_as_doc_1__document_0__original=document.original_id, # doc is related to passed document
                                   rels_as_doc_1__relationship=relationship) # AND relation type is correct
    tdc = len(docs)
  except:
    docs = []
  return _render_documents(docs, record, pha, tdc)


def document_rels(request, record, document_id_0, rel, document_id_1=None):
  """
  create a new document relationship, either with paylod of a new document, or between existing docs.
  2010-08-15: removed external_id and pha parameters as they are never set.
  That's for create_by_rel
  """
  try:
    document_0    = Document.objects.get(id = document_id_0)
    relationship  = DocumentSchema.objects.get(type= DocumentSchema.expand_rel(rel))
    if document_id_1:
      document_1 = Document.objects.get(id = document_id_1)
    else:
      try:
        document_1 = _document_create(record=record, 
                                      creator=request.principal,
                                      content=request.raw_post_data,
                                      mime_type=utils.get_content_type(request))
      except:
        raise Http404
    DocumentRels.objects.create(document_0=document_0, document_1=document_1, relationship=relationship)
  except:
    raise Http404
  return DONE


@transaction.commit_on_success
def document_create_by_rel(request, record, document_id, rel):
  """Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views"""
  return _document_create_by_rel(request, record, document_id, rel)

@transaction.commit_on_success
def document_create_by_rel_with_ext_id(request, record, document_id, rel, pha, external_id):
  """Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views"""
  return _document_create_by_rel(request, record, document_id, rel, pha, external_id)

def _document_create_by_rel(request, record, document_id, rel, pha=None, external_id=None):
  """Create a document and relate it to an existing document, all in one call.
  
  FIXME: currently ignoring app_email
  """
  old_doc = _get_document(record=record, document_id=document_id)
  if not old_doc:
    raise Http404

  # no rels in app-specific docs
  full_external_id = Document.prepare_external_id(external_id, pha=pha, pha_specific = False)

  try:
    # create the doc
    new_doc = _document_create( record = record, 
                                creator = request.principal,
                                pha = None,
                                content = request.raw_post_data,
                                external_id = full_external_id)
    # create the rel
    DocumentRels.objects.create(document_0 = old_doc, 
                                document_1 = new_doc, 
                                relationship = DocumentSchema.objects.get(type=DocumentSchema.expand_rel(rel)))
  except:
    raise Http404
  return DONE

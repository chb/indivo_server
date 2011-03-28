"""
Indivo Views -- Documents
"""

import urllib2
import hashlib

from indivo.lib import utils

from indivo.views.base import *
from indivo.document_processing.document_utils import DocumentUtils
from indivo.document_processing.document_processing import DocumentProcessing
from django.core.files.base import ContentFile


from django.db.models import Count


PHA, RECORD, CREATOR, MIME_TYPE, EXTERNAL_ID, ORIGINAL_ID, CONTENT, DIGEST, SIZE, TYPE, REPLACES, STATUS  = (
  'pha', 'record', 'creator', 'mime_type', 'external_id', 'original_id', 'content', 'digest', 'size', 'type', 'replaces', 'status')

##
## The following calls need to be optimized and not done at load time
##
def _set_doc_latest(doc):
  docutils_obj = DocumentUtils()
  latest = docutils_obj.get_latest_doc(doc.id)
  doc.latest(latest.id, latest.created_at, latest.creator.email)

def _get_doc_relations(doc):
  relates_to = doc.rels_as_doc_0.values('relationship__type').annotate(count=Count('relationship'))
  is_related_from = doc.rels_as_doc_1.values('relationship__type').annotate(count=Count('relationship'))
  return relates_to, is_related_from
  

def _render_documents(docs, record, pha, tdc, format_type='xml'):
  # tdc: Total Document Count
  if docs:
    for doc in docs:
      if doc.id:
        _set_doc_latest(doc)
        doc.relates_to, doc.is_related_from = _get_doc_relations(doc)

  return utils.render_template('documents', {  'docs'    : docs, 
                                               'record'  : record, 
                                               'pha'     : pha, 
                                               'tdc'     : tdc}, 
                                                type=format_type)

def _get_document(record=None, carenet=None, document_id=None, pha=None, external_id=None):
  """Get a document with the given doc id/(external id and pha) and record"""
  if carenet:
    record = carenet.record
  
  doc = None
  try:
    if document_id:
      doc = Document.objects.get(record=record, pha=pha, id=document_id)
    elif external_id:
      doc = Document.objects.get(record=record, pha=pha, external_id=external_id)
  except Document.DoesNotExist:
    return None
  return doc

def _document_create(creator, content, pha, record,
                     replaces_document=None, external_id=None, mime_type=None,
                     status = None):
  """ Create an Indivo Document

  This is called for both document creation within a record
    and document creation within a record for a specific application.

  The PHA argument, if non-null, indicates app-specificity only.
  By this point, the external_id should be fully formed.

  FIXME: figure out the transactional aspect here

  If status is specified, then it is used, otherwise it is not specified and the DB does its default thing.
  """
  new_doc = None

  # Overwrite content if we are replacing an existing PHA doc
  if pha and replaces_document:
    replaces_document.replace(content, mime_type)
  
  # Create new document
  else:
    creator = creator.effective_principal
    doc_args = {  PHA         : pha,
                  RECORD      : record,
                  CREATOR     : creator,
                  MIME_TYPE   : mime_type,
                  EXTERNAL_ID : external_id,
                  REPLACES    : replaces_document,
                  CONTENT     : content,
                  ORIGINAL_ID : replaces_document.original_id if replaces_document else None
                  }
    if status:
      create_args[STATUS] = status

    # create the document
    new_doc = Document.objects.create(**doc_args)

    # Save the binary file
    if DocumentProcessing(content, mime_type).is_binary:
      file = ContentFile(content)
      new_doc.content_file.save(new_doc.id, file)    

    # Mark old doc as replaced
    if replaces_document:
      replaces_document.replaced_by = new_doc
      replaces_document.save()
    
  # return new doc if we have it, otherwise updated old doc
  return new_doc or replaces_document

def __local_document_create(request, record, pha, external_id, existing_doc):
  """
  This function only serves document_create and document_create_or_update
  The pha argument is null for medical data, non-null for app-specific
  The external_id is expected to be already adjusted
  """
  try:
    doc = _document_create(record              = record, 
                          creator             = request.principal,
                          pha                 = pha, 
                          content             = request.raw_post_data, 
                          external_id         = external_id,
                          replaces_document   = existing_doc,
                          mime_type           = utils.get_content_type(request))
  except ValueError, e:
    return HttpResponseBadRequest("the document submitted is malformed:" + str(e))

  _set_doc_latest(doc)
  return utils.render_template('document', {'record'  : doc.record, 
                                            'doc'     : doc, 
                                            'pha'     : pha }) 


@commit_on_200
def document_create(request, record, pha=None, document_id=None, external_id=None):
  """
  Create a document, possibly with the given external_id
  This call is ONLY made on NON-app-specific data,
  so the PHA argument is non-null only for specifying an external_id
  """
  return __local_document_create(request, record, pha=None,
                                 external_id = Document.prepare_external_id(external_id, pha),
                                 existing_doc=None)

@commit_on_200
def document_create_by_ext_id(request, record, pha, external_id):
  """
  Create a document with the given external_id
  Same as document_create: this function exists
  to preserve the 1:1 mapping from functions to views
  """
  return __local_document_create(request, record, pha=None,
                                 external_id=Document.prepare_external_id(external_id, pha),
                                 existing_doc=None)

@commit_on_200
def app_document_create_or_update(request, pha, document_id):
  """For 1:1 mapping from views: calls document_create_or_update()"""
  return document_create_or_update(request, pha=pha, document_id=document_id)

@commit_on_200
def app_document_create(request, pha):
  """For 1:1 mapping from views: calls document_create_or_update()"""
  return document_create_or_update(request, pha=pha)

@commit_on_200
def app_document_create_or_update_ext(request, pha, external_id):
  """For 1:1 mapping from views: calls document_create_or_update()"""
  return document_create_or_update(request, pha, external_id=external_id)

@commit_on_200
def record_app_document_create(request, record, pha):
  """For 1:1 mapping from views: calls document_create_or_update()"""
  return document_create_or_update(request, pha, record=record)

@commit_on_200
def record_app_document_create_or_update_ext(request, record, pha, external_id):
  """For 1:1 mapping from views: calls document_create_or_update()"""
  return document_create_or_update(request, pha, record=record, external_id=external_id)

def document_create_or_update(request, pha, record=None, document_id=None, external_id=None):
  """
  Create a document, possibly with the given external_id
  This call is ONLY made on app-specific data,
  and the pha argument indicates the app-specificity
  """
  existing_doc = None

  # set the external ID up properly
  full_external_id = Document.prepare_external_id(external_id, pha,
                                                  pha_specific=True, record_specific= (record != None))

  if document_id:
    existing_doc = _get_document(record=record, document_id=document_id, pha=pha)
  elif external_id:
    existing_doc = _get_document(record=record, pha=pha, external_id=full_external_id)

  return __local_document_create(request, record, pha, full_external_id, existing_doc)


def record_app_specific_document(request, record, pha, document_id):
  """Retrieve a record-app-specific document: calls document()"""
  return document(request, document_id, record=record, pha=pha)


def app_specific_document(request, pha, document_id):
  """Retrive an app-specific document: calls document()"""
  return document(request, document_id, pha=pha)


def record_specific_document(request, record, document_id):
  """Retrieve a record-specific document: calls document()"""
  return document(request, document_id, record=record)

def document(request, document_id, record=None, pha=None):
  """Retrieve a document | Retrieval with external_id is not permitted"""
  document = _get_document(pha=pha, record=record, document_id=document_id)
  if not document or \
        (pha and document.pha != pha):
    raise Http404
  
  return _render_document(document)

def _render_document(document):
  # no content, must be a file
  if not document.content:
    return HttpResponse(document.content_file, mimetype=document.mime_type)

  return HttpResponse(document.content, mimetype="application/xml")


@marsloader
def app_document_list(request, pha, limit, offset, status, order_by='created_at'):
  """For 1:1 mapping of URLs to views. Calls document_list"""
  return document_list(request, limit, offset, status, order_by, pha=pha)

@marsloader
def record_document_list(request, record, limit, offset, status, order_by='created_at'):
  """For 1:1 mapping of URLs to views. Calls document_list"""
  return document_list(request, limit, offset, status, order_by, record=record)

@marsloader
def record_app_document_list(request, record, pha, limit, offset, status, order_by='created_at'):
  """For 1:1 mapping of URLs to views. Calls document_list"""
  return document_list(request, limit, offset, status, order_by, record=record, pha=pha)

def document_list(request, limit, offset, status, order_by='created_at', record=None, pha=None):
  """
  As of 2010-08-16, type is no longer part of the URL, it's only in the GET
  query parameters
  """
  # SZ: CLEAN CODE!
  # SZ: CLEAN CODE!
  # SZ: CLEAN CODE!
  type = request.GET.get('type', None)
  type = DocumentProcessing.expand_schema(type)

  try:
    if type:
      try:
        type_obj = DocumentSchema.objects.get(type=type)
        if record:
          docs = record.documents.filter(type=type_obj, 
                  replaced_by=None, status=status, pha=pha).order_by(order_by)
        else:
          docs = Document.objects.filter(type=type_obj, 
                  pha=pha, replaced_by=None, status=status).order_by(order_by)
        return _render_documents(docs, record, pha, docs.count())
      except DocumentSchema.DoesNotExist:
        raise Http404
    docs = Document.objects.filter(record=record, 
            replaced_by=None, pha=pha, status=status).order_by(order_by)
  except:
    docs = []
  return _render_documents(docs[offset:offset+limit], record, pha, len(docs))

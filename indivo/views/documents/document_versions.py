"""
.. module:: views.document.document_versions
   :synopsis: Indivo view implementations related to document versioning.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from indivo.views.documents.document import _document_create, _render_documents, _set_doc_latest, _get_document

@transaction.commit_on_success
def document_version(request, record, document_id):
  """ Create a new version of a record-specific document.

  Calls into 
  :py:meth:`~indivo.views.documents.document_versions._document_version`.

  """

  return _document_version(request, record, document_id)

@transaction.commit_on_success
def document_version_by_ext_id(request, record, document_id, pha, external_id):
  """ Create a new version of a record-specific document and assign it an external id.

  Calls into 
  :py:meth:`~indivo.views.documents.document_versions._document_version`.

  """

  return _document_version(request, record, document_id, pha=pha, external_id=external_id)

def _document_version(request, record, document_id, pha=None, external_id=None):
  """ Create a new version of a record-specific document. 

    **ARGUMENTS:**
  
  * *request*: The incoming Django HttpRequest object. ``request.POST`` must 
    consist of a raw string containing the new document content.
  
  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` to which
    the old document is scoped, and to which the new document will be scoped.

  * *document_id*: The internal identifier of the old document. The old document
    must be at the latest version, or the call will fail.

  * *external_id*: The external identifier to assign to the new document.

  * *pha*: The :py:class:`~indivo.models.apps.PHA` object used
    to scope *external_id*, if present.

  **RETURNS:**

  * An HttpResponse object with an XML string containing metadata on the new
    document on success.

  * :http:statuscode:`400` if the old document has previously been replaced 
    by a newer version.

  **RAISES:**

  * :py:exc:`django.http.Http404` if *document_id* doesn't
    identify an existing document, or if document creation fails (odd behavior).

  """

  old_document = _get_document(record=record, document_id=document_id)
  if not old_document:
    raise Http404

  # Can't version an already versioned document
  if old_document.replaced_by:
    return HttpResponseBadRequest("Can't version a document that has already been versioned. Get the latest version of the document.")


  full_external_id = Document.prepare_external_id(external_id, pha)
  try:
    new_doc = _document_create(record=record, 
                               creator=request.principal, 
                               content=request.body,
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
def document_versions(request, record, document_id, query_options):
  """ Retrieve the versions of a document.

  **ARGUMENTS:**
  
  * *request*: The incoming Django HttpRequest object.
  
  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` to which
    the document is scoped.

  * *document_id*: The internal identifier of the document. 

  * *limit*, *offset*, *status*, *order_by*: Standard paging and filtering 
    arguments. See :py:func:`~indivo.lib.view_decorators.marsloader`
    or :doc:`/query-api`.

  **RETURNS:**

  * An HttpResponse object with an XML string containing metadata on all versions
    of the document, including the passed *document_id*, on success.

  **RAISES:**

  * :py:exc:`django.http.Http404` if *document_id* doesn't
    identify an existing document.

  """

  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  try:
    docs = Document.objects.filter( original  = document.original_id, 
                                    status    = query_options['status']).order_by(query_options['order_by'])
  except:
    raise Http404

  offset = query_options['offset']
  limit = query_options['limit']
  
  total_count = docs.count()
  if limit:
      docs = docs[offset:offset+limit]
  return _render_documents(docs, record, None, total_count)

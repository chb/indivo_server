"""
.. module:: views.document.document_rels
   :synopsis: Indivo view implementations related to document relations

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from indivo.views.documents.document import _document_create, _render_documents, _get_document

@marsloader()
def get_documents_by_rel(request, record, document_id, rel, limit, offset, status, order_by='id', pha=None):
  """ Get all documents related to the passed document_id by a relation of the passed relation-type.

  Includes relationships to other versions of *document_id*.
  Paging operators are NOT IMPLEMENTED.

  **ARGUMENTS:**

  * *request*: The incoming Django HttpRequest object.
  
  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` that
    the document is scoped to.

  * *document_id*: The internal document identifier for the source document.

  * *rel*: The relationship type to filter related documents by (as a string).

  * *limit*, *offset*, *status*, *order_by*: Standard paging and filtering 
    arguments. See :py:func:`~indivo.lib.view_decorators.marsloader`
    or :doc:`/query-api`.

    .. Note:: 
    
       Paging operators are not implemented for this call currently. Passing
       them into the function will have no effect on output.

  * *pha*: The :py:class:`~indivo.models.apps.PHA` object that the
    source document is scoped to, if applicable.

  **RETURNS:**

  * An HttpResponse object with an XML string listing related documents
    on success.

  **RAISES:**

  * :py:exc:`django.http.Http404` if *document_id*
    doesn't identify an existing document scoped to *record*.

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


def document_rels(request, record, document_id_0, rel, document_id_1):
  """ Create a new relationship between two existing documents.

  **ARGUMENTS:**

  * *request*: The incoming Django HttpRequest object.
  
  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` that
    the documents are scoped to.

  * *document_id_0*: The internal document identifier for the source document.

  * *rel*: The relationship type between the two documents (as a string).

  * *document_id_1*: The internal document identifier for the related document.

  **RETURNS:**

  * :http:statuscode:`200` on success.

  **RAISES:**

  * :py:exc:`django.http.Http404` if either *document_id_0* or *document_id_1*
    don't identify an existing document scoped to *record*, or if *rel* doesn't
    identify a valid relationship type.

  """
  try:
    document_0    = Document.objects.get(id = document_id_0)
    relationship  = DocumentSchema.objects.get(type= DocumentSchema.expand_rel(rel))
    document_1 = Document.objects.get(id = document_id_1)

    DocumentRels.objects.create(document_0=document_0, document_1=document_1, relationship=relationship)
  except Document.DoesNotExist:
    raise Http404
  except DocumentSchema.DoesNotExist:
    raise Http404
  return DONE


@transaction.commit_on_success
def document_create_by_rel(request, record, document_id, rel):
  """ Create a document and relate it to an existing document.

  Calls into :py:meth:`~indivo.views.documents.document_rels._document_create_by_rel`.

  """

  return _document_create_by_rel(request, record, document_id, rel)

@transaction.commit_on_success
def document_create_by_rel_with_ext_id(request, record, document_id, rel, pha, external_id):
  """ Create a document, assign it an external id, and relate it to an existing document.

  Calls into :py:meth:`~indivo.views.documents.document_rels._document_create_by_rel`.

  """

  return _document_create_by_rel(request, record, document_id, rel, pha, external_id)

def _document_create_by_rel(request, record, document_id, rel, pha=None, external_id=None):
  """ Create a document and relate it to an existing document.

  **ARGUMENTS:**

  * *request*: The incoming Django HttpRequest object. ``request.POST`` must
    contain the raw content of the new document.
  
  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` to
    which to scope the new document, and to which the source document is scoped.

  * *document_id*: The internal document identifier for the source document.

  * *rel*: The relationship type to establish between the source document and the
    new document (as a string).

  * *pha*: The :py:class:`~indivo.models.apps.PHA` object that 
    scopes the external_id, if present.

  * *external_id*: The external identifier to assign to the newly created document.

  **RETURNS:**

  * :http:statuscode:`200` on success.

  * :http:statuscode:`400` if the new document content is invalid

  **RAISES:**

  * :py:exc:`django.http.Http404` if *document_id*
    doesn't identify an existing document scoped to *record*, or if
    *rel* doesn't identify an valid relationship type.  

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
  except DocumentSchema.DoesNotExist:
    raise Http404
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
  return DONE

"""
.. module:: views.document.document_delete
   :synopsis: Indivo view implementations related to document deletion.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from indivo.views.documents.document import _get_document

def app_document_delete(request, pha, document_id):
  """ Delete an app-specific document. 

  No restrictions, since this storage is managed by the app.

  Calls into
  :py:meth:`~indivo_server.indivo.views.documents.document_delete._document_delete`.

  """

  return _document_delete(document_id, pha=pha)

def record_app_document_delete(request, record, pha, document_id):
  """ Delete a record-app-specific document. 

  No restrictions, since this storage is managed by the app.

  Calls into
  :py:meth:`~indivo_server.indivo.views.documents.document_delete._document_delete`.

  """

  return _document_delete(document_id, pha=pha, record=record)


def _document_delete(document_id, pha=None, record=None):
  """ Delete a document.

  **ARGUMENTS:**

  * *document_id*: The internal identifier of the document to delete.
  
  * *pha*: If the document to delete is scoped to an app, this
    :py:class:`~indivo_server.indivo.models.apps.PHA` instance refers to the app.

  * *record*: If the document to delete is scoped to a record, this
    :py:class:`~indivo_server.indivo.models.records_and_documents.Record` 
    instance refers to the record.
  
  **RETURNS:**
  
  * :http:statuscode:`200` on success.

  **RAISES:**
  
  * :py:exc:`django.http.Http404` if the arguments don't identify an existing
    document.

  """

  document = _get_document(record=record, pha=pha, document_id=document_id)
  if not document:
    raise Http404

  document.delete()
  return DONE

def documents_delete(request, record):
  """ Delete all documents associated with a record.

  **ARGUMENTS:**

  * *request*: The incoming Django HttpRequest object.
  
  * *record*: The 
    :py:class:`~indivo_server.indivo.models.records_and_documents.Record` to
    purge of documents.

  **RETURNS:**
  
  * :http:statuscode:`200` on success.

  """

  Document.objects.filter(record=record).delete()
  return DONE

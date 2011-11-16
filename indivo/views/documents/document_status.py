"""
.. module:: views.document.document_status
   :synopsis: Indivo view implementations related to document status.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from indivo.views.documents.document import _get_document

@transaction.commit_on_success
def document_set_status(request, record, document_id):
  """ Set the status of a record-specific document.

  **ARGUMENTS:**
  
  * *request*: The incoming Django HttpRequest object. ``request.POST`` must 
    contain:
    
    * *status* The new status for the document. Must identify an existing
      :py:class:`~indivo_server.indivo.models.status.StatusName` object.
    
    * *reason* The reason for the status change
  
  * *record*: The 
    :py:class:`~indivo_server.indivo.models.records_and_documents.Record` that
    the document is scoped to.

  * *document_id*: The internal identifier of the document whose status is being
    altered.

  **RETURNS:**

  * :http:statuscode:`200` on success.

  * :http:statuscode:`400` if ``request.POST`` is missing arguments.

  **RAISES:**

  * :py:exc:`django.http.Http404` if *document_id* doesn't
    identify an existing document scoped to *record*.

  """

  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  status_str, reason_str = 'status', 'reason'
  try:
    document.set_status(request.principal, 
                        request.POST[status_str],
                        request.POST[reason_str])
  except:
    return HttpResponseBadRequest()

  return DONE

def document_status_history(request, record, document_id):
  """ List all changes to a document's status over time.

  **ARGUMENTS:**
  
  * *request*: The incoming Django HttpRequest object.
  
  * *record*: The 
    :py:class:`~indivo_server.indivo.models.records_and_documents.Record` that
    the document is scoped to.

  * *document_id*: The internal identifier of the document for which to get 
    status history.

  **RETURNS:**

  * A :py:class:`django.http.HttpResponse` object containing an XML string
    listing status changes for the document.

  **RAISES:**

  * :py:exc:`django.http.Http404` if *document_id* doesn't
    identify an existing document scoped to *record*.

  """

  document = _get_document(record=record, document_id=document_id)
  if not document:
    raise Http404

  return render_template('document_status_history', 
          { 'document_id'      : document.id,
            'document_history' : DocumentStatusHistory.objects.filter(
                                  record    = record.id, 
                                  document  = document.id)})

"""
.. module:: views.document.document_label
   :synopsis: Indivo view implementations related to document labeling.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from indivo.views.documents.document import _render_documents, _get_document

def app_document_label(request, pha, document_id):
  """ Set the label of an app-specific document.

  Calls into 
  :py:meth:`~indivo_server.indivo.views.documents.document_label._document_label`.

  """

  return _document_label(request, pha=pha, document_id=document_id, app_specific=True)


def record_app_document_label(request, record, pha, document_id):
  """ Set the label of a record-app-specific document.

  Calls into 
  :py:meth:`~indivo_server.indivo.views.documents.document_label._document_label`.

  """

  return _document_label(request, record=record, pha=pha, document_id=document_id, app_specific=True)


def record_document_label(request, record, document_id):
  """ Set the label of a record-specific document.

  Calls into 
  :py:meth:`~indivo_server.indivo.views.documents.document_label._document_label`.

  """

  return _document_label(request, record=record, document_id=document_id, app_specific=False)


def record_document_label_ext(request, record, document=None, external_id=None, pha=None, app_specific=False):
  """ Set the label of a record-specific document, specified by external id.

  Calls into 
  :py:meth:`~indivo_server.indivo.views.documents.document_label._document_label`.

  """

  return _document_label(request, record, document, external_id, pha, app_specific)

def _document_label(request, record=None, document_id=None, external_id=None, pha=None, app_specific=False):
  """ Set a document's label.

  **ARGUMENTS:**
  
  * *request*: The incoming Django HttpRequest object. ``request.POST`` must 
    consist of a raw string containing the new label to assign.
  
  * *record*: The 
    :py:class:`~indivo_server.indivo.models.records_and_documents.Record` that
    the document is scoped to, if applicable.

  * *document_id*: The internal identifier of the document to re-label.

    .. Note::

       One of *external_id* or *document_id* MUST be passed to this function, 
       or it cannot retrieve a unique document.

  * *external_id*: The external identifier of the document to re-label.

    .. Note::

       One of *external_id* or *document_id* MUST be passed to this function, 
       or it cannot retrieve a unique document.

  * *pha*: The :py:class:`~indivo_server.indivo.models.apps.PHA` object that the
    document is scoped to. Also serves to scope *external_id*, if present and
    *app_specific* is ``True``.

  * *app_specific*: Whether or not the document is app-specific. The mere presence
    of the *pha* argument isn't enough to satisfy this question, as *pha* might
    have been passed in only to scope an external id for a non-app-specific
    document.

  **RETURNS:**

  * An HttpResponse object with an XML string describing the re-labeled document
    on success.

  **RAISES:**

  * :py:exc:`django.http.Http404` if neither *document_id* nor *external_id*
    identify an existing document.

  """

  label = request.raw_post_data

  # Get the document
  full_external_id = Document.prepare_external_id(external_id, pha, pha_specific = app_specific)
  if not app_specific:
    pha = None
  document = _get_document(record=record, document_id=document_id, pha=pha, external_id=full_external_id)
    
  if not document:
    raise Http404

  document.label = label
  document.save()

  return _render_documents([document], record, pha, 1)

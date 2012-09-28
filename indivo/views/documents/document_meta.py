"""
.. module:: views.document.document_meta
   :synopsis: Indivo view implementations related to document metadata

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from indivo.views.documents.document import _set_doc_latest, _get_document


def update_document_meta(request, record, document_id):
  """ Set metadata fields on a document. NOT IMPLEMENTED. """

  # Does Nothing
  return DONE


def carenet_document_meta(request, carenet, document_id):
  """ Fetch the metadata of a record-specific document via a carenet.

  Calls into 
  :py:meth:`~indivo.views.documents.document_meta._document_meta`.

  """

  document = _get_document(carenet=carenet, document_id=document_id)
  return _document_meta(carenet=carenet, document=document)


def record_document_meta(request, record, document_id):
  """ Fetch the metadata of a record-specific document.

  Calls into 
  :py:meth:`~indivo.views.documents.document_meta._document_meta`.

  """

  document = _get_document(record=record, document_id=document_id)
  return _document_meta(record=record, document=document)


def record_document_meta_ext(request, record, pha, external_id):
  """ Fetch the metadata of a record-specific document identified by external id.

  Calls into 
  :py:meth:`~indivo.views.documents.document_meta._document_meta`.

  """

  return _document_meta(record=record, pha=pha, external_id=external_id)


def app_document_meta(request, pha, document_id):
  """ Fetch the metadata of an app-specific document.

  Calls into 
  :py:meth:`~indivo.views.documents.document_meta._document_meta`.

  """
  """For 1:1 mapping of URLs to views. Calls _document_meta"""
  document = _get_document(pha=pha, document_id=document_id)
  return _document_meta(pha=pha, document=document, app_specific=True)

def app_document_meta_ext(request, pha, external_id):
  """ Fetch the metadata of an app-specific document identified by external id.

  Calls into 
  :py:meth:`~indivo.views.documents.document_meta._document_meta`.

  """

  return _document_meta(pha=pha, external_id=external_id, app_specific=True)


def record_app_document_meta(request, record, pha, document_id):
  """ Fetch the metadata of a record-app-specific document.

  Calls into 
  :py:meth:`~indivo.views.documents.document_meta._document_meta`.

  """

  document = _get_document(record=record, pha=pha, document_id=document_id)
  return _document_meta(record=record, document=document, pha=pha, app_specific=True)


def record_app_document_meta_ext(request, record, pha, external_id):
  """ Fetch the metadata of a record-app-specific document identified by external id.

  Calls into 
  :py:meth:`~indivo.views.documents.document_meta._document_meta`.

  """

  return _document_meta(record=record, pha=pha, external_id=external_id, app_specific=True)


def _document_meta(record=None, carenet=None, document=None, pha=None, external_id=None, app_specific=False):
  """ Fetch the metadata of a single document.
  
  Metadata includes:
  
  * id

  * date created
  
  * creator 

  * the document that replaced this one

  * the document that this one replaces

  * the original document in the version chain

  * the latest document in the version chain

  * label

  * current status

  * nevershare status

  * related documents
  

  **ARGUMENTS:**
  
  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` that
    the document is scoped to, if applicable.

  * *carenet*: The 
    :py:class:`~indivo.models.shares.Carenet` that
    the document is shared into, if applicable.

  * *document*: The document to get metadata for, if it has been prefetched.

    .. Note::

       One of *external_id* or *document* MUST be passed to this function, 
       or it cannot retrieve a unique document.

  * *pha*: The :py:class:`~indivo.models.apps.PHA` object that the
    document is scoped to. Also serves to scope *external_id*, if present and
    *app_specific* is ``True``.

  * *external_id*: The external identifier of the document to re-label.

    .. Note::

       One of *external_id* or *document* MUST be passed to this function, 
       or it cannot retrieve a unique document.

  * *app_specific*: Whether or not the document is app-specific. The mere presence
    of the *pha* argument isn't enough to satisfy this question, as *pha* might
    have been passed in only to scope an external id for a non-app-specific
    document.

  **RETURNS:**

  * An HttpResponse object with an XML string describing the document metadata
    on success.

  **RAISES:**

  * :py:exc:`django.http.Http404` if *document* isn't passed and *external_id*
    doesn't identify an existing document.

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

  return render_template('single_document', {'doc' : document, 'record': document.record})

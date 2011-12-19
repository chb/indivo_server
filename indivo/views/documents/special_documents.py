from indivo.views.base import *
from indivo.views.documents.document import _document_create, _set_doc_latest

def special_document(request, record, document_alias):
  """ Unimplemented. """
  if document_alias == 'demographics':
    pass
  if document_alias == 'contact':
    pass

  # no such thing
  raise Http404
  
def special_document_update(request, record, document_alias):
  """ Unimplemented. """
  if document_alias == 'demographics':
    pass
  if document_alias == 'contact':
    pass

  # no such thing
  raise Http404

def get_special_doc(record, carenet, special_document):
  """ Fetch a special document from either a record or a carenet.

  **ARGUMENTS:**

  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` from 
    which to fetch the special document.

    .. Note::

       Either *record* or *carenet* must be non-empty.

  * *carenet*: The 
    :py:class:`~indivo.models.shares.Carenet` from 
    which to fetch the special document.

    .. Note::

       Either *record* or *carenet* must be non-empty.


  * *special_document*: The type of special document to fetch. Options are 
    ``demographics`` or ``contact``.

  **RETURNS:**

  * The special document as a
    :py:class:`~indivo.models.records_and_documents.Document`
    instance, if the special document exists.

  * ``None``, if *record* or *carenet* hasn't been assigned a special
    document of type *special_document*.

  **RAISES:**

  * :py:exc:`ValueError` if neither *record* nor *carenet* was passed.

  """

  if record is None and carenet is None:
    raise ValueError("carenet or record must be non-null")

  the_doc = None
  
  docbox = record or carenet
  if special_document == 'demographics':
    the_doc = docbox.demographics
  if special_document == 'contact' :
    the_doc = docbox.contact
    
  return the_doc

def set_special_doc(record, special_document, new_doc):
  """ Set a record to point to a different existing special_document.

  Also updates the label of *record* to the full_name in the new 
  contact document.

  **ARGUMENTS:**

  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` to 
    update.

  * *special_document*: The type of special document to update. Options are 
    ``demographics`` or ``contact``.

  * *new_doc*: The
    :py:class:`~indivo.models.records_and_documents.Document` to 
    point to.

  **RETURNS:**

  * ``None``

  """

  if special_document == 'demographics':
    record.demographics = new_doc
  if special_document == 'contact' :
    record.contact = new_doc

    # update the label
    record.label = Contacts.from_xml(new_doc.content).full_name
  record.save()


def read_special_document(request, special_document, record):
  """ Read a special document from a record.

  Calls into 
  :py:meth:`~indivo.views.documents.special_documents._read_special_document`.
  
  """

  return _read_special_document(request, special_document, record=record)

def read_special_document_carenet(request, special_document, carenet):
  """ Read a special document from a carenet.

  Calls into 
  :py:meth:`~indivo.views.documents.special_documents._read_special_document`.

  """

  return _read_special_document(request, special_document, carenet=carenet)

def _read_special_document(request, special_document, record=None, carenet=None):
  """ Read a special document.

  Calls into 
  :py:meth:`~indivo.views.documents.special_documents.get_special_doc`.

  """

  doc = get_special_doc(record, carenet, special_document)
  if not doc:
    raise Http404
  return HttpResponse(doc.content, mimetype="application/xml")


@transaction.commit_on_success
def save_special_document(request, record, special_document):
  """ Create or update a special document on a record.

  **ARGUMENTS:**

  * *request*: The incoming Django HttpRequest object. ``request.POST`` must 
    consist of a raw string containing the new document content.

  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` from 
    which to fetch the special document.

  * *special_document*: The type of special document to update. Options are 
    ``demographics`` or ``contact``.

  **RETURNS:**

  * a :py:class:`django.http.HttpResponse` containing Metadata XML on the
    newly created document.

  * :http:statuscode:`400` if the new document content didn't validate.

  """

  doc = get_special_doc(record, carenet=None, special_document=special_document)

  # this will do the right thing in terms of replacement
  try:
    new_doc = _document_create(record=record, 
                               creator=request.principal, 
                               content=request.raw_post_data,
                               pha=None,
                               replaces_document=doc)
  except:
    return HttpResponseBadRequest('Invalid document: special documents must be valid XML')
    
  # update the record pointer
  set_special_doc(record, special_document, new_doc)

  _set_doc_latest(new_doc)
  return render_template('document', { 'record'  : record, 
                                              'doc'     : new_doc, 
                                              'pha'     : None})

from indivo.views.base import *
from indivo.views.documents.document import _document_create, _set_doc_latest
from indivo.models import Demographics

def get_demographics(record_or_carenet):
  """ Fetch the demographics from either a record or a carenet.

  **ARGUMENTS:**

  * *record_or_carenet*: The 
    :py:class:`~indivo.models.records_and_documents.Record` or 
    :py:class:`~indivo.models.shares.Carenet` from which to fetch the demographics.

  **RETURNS:**

  * The demographics as a
    :py:class:`~indivo.models.Demographics`
    instance, if they exist.

  * ``None``, if *record* or *carenet* hasn't been assigned  demographics

  **RAISES:**

  * :py:exc:`ValueError` if *record_or_carenet* is None.

  """

  if record_or_carenet is None:
    raise ValueError("carenet or record must be non-null")

  the_doc = None
  the_doc = record_or_carenet.demographics
    
  return the_doc

def read_demographics(request, record):
  """ Read demographics from a record.

  Calls into 
  :py:meth:`~indivo.views.documents.special_documents._read_demographics`.
  
  """

  return _read_demographics(request, record)

def read_demographics_carenet(request, carenet):
  """ Read demographics from a carenet.

  Calls into 
  :py:meth:`~indivo.views.documents.special_documents._read_demographics`.

  """

  return _read_demographics(request, carenet)

def _read_demographics(request, record_or_carenet):
  """ Read demographics from a record or carenet.

  Calls into 
  :py:meth:`~indivo.views.documents.special_documents.get_demographics`.

  """
  demographics = get_demographics(record_or_carenet)
  if not demographics:
    raise Http404

  response_format = request.GET.get("response_format", 'application/rdf+xml')
  
  if response_format == 'application/rdf+xml':
      result = demographics.as_rdf()
  elif response_format == 'application/json':
      result = demographics.as_json()
  elif response_format == 'application/xml':
      result = demographics.as_xml()
  else:
      return HttpResponseBadRequest('format not supported')
  
  return HttpResponse(result,  mimetype=response_format)

@transaction.commit_on_success
def set_demographics(request, record):
  """ Create or update demographics on a record.

  **ARGUMENTS:**

  * *request*: The incoming Django HttpRequest object. ``request.POST`` must 
    consist of a raw string containing the demographics content.

  * *record*: The 
    :py:class:`~indivo.models.records_and_documents.Record` from 
    which to fetch the demographics.

  **RETURNS:**

  * a :py:class:`django.http.HttpResponse` containing Metadata XML on the
    newly created document. TODO: what should we return now that we have a model

  * :http:statuscode:`400` if the new demographics content didn't validate.

  """
  
  # grab existing demographics
  demographics = get_demographics(record)
  demographics_doc = (demographics.document if demographics else None)

  # build new demographics
  try:
    new_demographics = Demographics.from_xml(request.raw_post_data)
  except Exception as e:
    return HttpResponseBadRequest(str(e))  

  # this will do the right thing in terms of replacement
  try:
    new_doc = _document_create(record=record, 
                               creator=request.principal, 
                               content=request.raw_post_data,
                               pha=None,
                               replaces_document=demographics_doc)
    new_demographics.document = new_doc
  except:
    return HttpResponseBadRequest('Invalid document: special documents must be valid XML')
    
  # update the record pointer
  new_demographics.save()
  record.demographics = new_demographics
  record.save()
  #TODO: used to be changing the record label to reflect updated demographics

  _set_doc_latest(new_doc)
  return render_template('document', { 'record'  : record, 
                                              'doc'     : new_doc, 
                                              'pha'     : None})

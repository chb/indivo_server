from lxml import etree
from indivo.models import *

def _record_create(creator, contact_xml, owner=None, principal_email=None, external_id=None):
  """ Create an Indivo record.

  request.POST must contain raw XML that is a valid Indivo Contact
  document (see :doc:`/schemas/contact-schema`).
  
  This call will create a new record containing the following 
  information:

  * *creator*: Corresponds to ``request.principal``.

  * *label*: The full name of the new record, specified in the
    contact document.

  * *owner*: Corresponds to ``request.principal``.

  * *external_id* An external identifier for the record, if 
    passed in.

  Additionally, this call will create a Contact document for the record.

  Will return the record on success, or raise a ValueError if the contact 
  data in request.POST was empty or invalid XML.
  
  """

  if not owner:
    owner = creator

  # If the xml data is not valid return an HttpResponseBadRequest Obj
  xml_data = contact_xml
  try:
    etree.XML(xml_data)
  except:
    raise ValueError("Contact XML not valid")

  record_external_id = Record.prepare_external_id(external_id, principal_email)
    
  if external_id:
    record , created_p = Record.objects.get_or_create(
      external_id = record_external_id,
      defaults = {
        'creator' : creator,
        'label' : Contacts.from_xml(xml_data).full_name,
        'owner' : owner})
  else:
    record = Record.objects.create(
      external_id = record_external_id,
      creator = creator,
      label = Contacts.from_xml(xml_data).full_name,
      owner = owner)
    created_p = True

  # only set up the new contact document if the record is new
  # otherwise just return the existing record
  if created_p:
    # Create default carenets for this particular record
    record.create_default_carenets()

    # Create the contact document
    # use the same external ID as for the record
    # since those are distinct anyways
    doc_external_id = record_external_id

    doc = _document_create( record      = record,
                            creator     = creator,
                            pha         = None,
                            content     = xml_data,
                            external_id = doc_external_id)
      
    # save the contact document as the special contact doc
    record.contact = doc
    record.save()
    
  return record

def _account_create(creator, account_id='', full_name='', contact_email=None,
                    primary_secret_p="1", secondary_secret_p="0", **unused_args):
    """ Create a new account, and send out initialization emails.
    
    Required Parameters:
    
    * *creator*: The creator of the account. Usually ``request.principal``

    * *account_id*: an identifier for the new address. Must be formatted
      as an email address.
    
    Optional Parameters:
    
    * *full_name*: The full name to associate with the account. Defaults
      to the empty string.
    
    * *contact_email*: A valid email at which the account holder can 
      be reached. Defaults to the *account_id* parameter.
    
    * *primary_secret_p*: ``0`` or ``1``. Whether or not to associate 
      a primary secret with the account. Defaults to ``1``.
    
    * *secondary_secret_p*: ``0`` or ``1``. Whether or not to associate
      a secondary secret with the account. Defaults to ``0``.

    * *unused_args*: currently ignored.
    
    After creating the new account, this call generates secrets for it,
    and then emails the user (at *contact_email*) with their activation
    link, which contains the primary secret.
    
    This call will return the new account on success, and raise a ValueError
    if *account_id* isn't provided or isn't a valid email address, or if an 
    account already exists with an id matching *account_id*.
      
    """

    if not account_id or not utils.is_valid_email(account_id):
        raise ValueError("Account ID not valid")

    if not contact_email:
        contact_email = account_id
    
    new_account, create_p = Account.objects.get_or_create(email=urllib.unquote(account_id).lower().strip())
    if create_p:
        
        # generate a secondary secret or not? Requestor can say no.
        # trust model makes sense: the admin app requestor only decides whether or not 
        # they control the additional interaction or if it's not necessary. They never
        # see the primary secret.
        
        new_account.full_name = full_name
        new_account.contact_email = contact_email
        
        new_account.creator = creator
        
        primary_secret_p    = (primary_secret_p == "1")
        secondary_secret_p  = (secondary_secret_p == "0")
        
        # we don't allow setting the password here anymore
        new_account.save()
        
        if primary_secret_p:
            new_account.generate_secrets(secondary_secret_p = secondary_secret_p)
            try:
                new_account.send_secret()
            except Exception, e:
                logging.exception(e)
    
    # account already existed
    else:
        raise ValueError("An account with email address %s already exists." % account_id)

    return new_account


PHA, RECORD, CREATOR, MIME_TYPE, EXTERNAL_ID, ORIGINAL_ID, CONTENT, DIGEST, SIZE, TYPE, REPLACES, STATUS    = (
    'pha', 'record', 'creator', 'mime_type', 'external_id', 'original_id', 'content', 'digest', 'size', 'type', 'replaces', 'status')

def _document_create(creator, content, pha, record,
                                         replaces_document=None, external_id=None, mime_type=None,
                                         status = None):
    """ Create an Indivo Document.

    This is the lowest-level creation function called for all record- and/or 
    app-specific documents.

    The PHA argument, if non-null, indicates app-specificity only. By this point, 
    the external_id should be fully formed.

    If status is specified, then it is used, otherwise it is not specified and 
    the model's default value is used (i.e. ``active``).

    This function creates a new model instance, processing the document if 
    necessary, and storing it in the database (or in the file system, if the
    document is binary).

    **Arguments:**

    * *creator*: The :py:class:`~indivo.models.base.Principal`
        instance that is responsible for creating the document.

    * *content*: The raw content (XML or binary) of the document to be created.

    * *pha*: if the document is application-specific, this
        :py:class:`~indivo.models.apps.PHA` instance refers to the 
        application to which the document pertains.
    
    * *record*: if the document is record-specific, this
        :py:class:`~indivo.models.records_and_documents.Record`
        instance refers to the document's record.

    * *replaces_document*: If the new document will overwrite (via in-place update
        or versioning) an existing document, this 
        :py:class:`~indivo.models.records_and_documents.Document`
        instance references the old document to be overwritten.

    * *external_id*: the external identifier to assing to the new document, 
        if available. The identifier should already have been prepared using
        :py:meth:`~indivo.models.records_and_documents.Document.prepare_external_id`.

    * *mime_type*: the mime type of the new document, i.e. 
        :mimetype:`application/xml`.

    * *status*: The initial status of the new document. ``active`` by default.
     
    **Returns:**

    * A new instance of 
        :py:class:`~indivo.models.records_and_documents.Document`,
        on success. If the document was updated in place, and no new document was
        created, the old document is returned.

    **Raises:**
    
    * :py:exc:`ValueError`: if the document doesn't validate.
    
    * :py:exc:`django.db.IntegrityError`: if the arguments to this function
        violate a database unique constraint (i.e., duplicate external id).

        .. warning::

             If an :py:exc:`IntegrityError` is raised, it will invalidate the 
             current database transaction. Calling functions should handle this
             case and rollback the current transaction.

    """

    new_doc = None

    # Overwrite content if we are replacing an existing PHA doc
    if pha and replaces_document:
        replaces_document.replace(content, mime_type)
    
    # Create new document
    else:
        creator = creator.effective_principal
        doc_args = {PHA         : pha,
                    RECORD      : record,
                    CREATOR     : creator,
                    MIME_TYPE   : mime_type,
                    EXTERNAL_ID : external_id,
                    REPLACES    : replaces_document,
                    CONTENT     : content,
                    ORIGINAL_ID : replaces_document.original_id if replaces_document else None
                }
        if status:
            doc_args[STATUS] = status

        # create the document
        new_doc = Document.objects.create(**doc_args)

    # return new doc if we have it, otherwise updated old doc
    return new_doc or replaces_document

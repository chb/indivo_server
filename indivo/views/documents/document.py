"""
.. module:: views.document.document
     :synopsis: Indivo view implementations related to document creation and listing.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

import urllib2
import hashlib

from indivo.lib import utils

from indivo.views.base import *
from indivo.document_processing.document_utils import DocumentUtils
from indivo.document_processing.document_processing import DocumentProcessing

from django.db.models import Count
from django.db import IntegrityError, transaction


PHA, RECORD, CREATOR, MIME_TYPE, EXTERNAL_ID, ORIGINAL_ID, CONTENT, DIGEST, SIZE, TYPE, REPLACES, STATUS    = (
    'pha', 'record', 'creator', 'mime_type', 'external_id', 'original_id', 'content', 'digest', 'size', 'type', 'replaces', 'status')

##
## The following calls need to be optimized and not done at load time
##
def _set_doc_latest(doc):
    """ Set the 'latest version'-related fields on a document for rendering.

    This is computed at load-time before each rendering of document. It is 
    not pre-computed or stored in the DB.

    returns: None

    """

    docutils_obj = DocumentUtils()
    latest = docutils_obj.get_latest_doc(doc.id)
    doc.latest(latest.id, latest.created_at, latest.creator.email)

def _get_doc_relations(doc):
    """ Set the 'related documents'-related fields on a document for rendering.

    This is computed at load-time before each rendering of document. It is 
    not pre-computed or stored in the DB.

    returns: None

    """

    relates_to = doc.rels_as_doc_0.values('relationship__type').annotate(count=Count('relationship'))
    is_related_from = doc.rels_as_doc_1.values('relationship__type').annotate(count=Count('relationship'))
    return relates_to, is_related_from
    

def _render_documents(docs, record, pha, tdc, format_type='xml'):
    """ Lowlevel document rendering to response data.

    **Arguments:**
    
    * *docs*: An iterable of 
        :py:class:`~indivo.models.records_and_documents.Document`
        objects to be rendered.

    * *record*: The 
        :py:class:`~indivo.models.records_and_documents.Record`
        that every document in *docs* belongs to.

    * *pha*: The
        :py:class:`~indivo.models.apps.PHA` that *docs* are 
        scoped to.

    * *tdc*: The total document count of objects to render (i.e., ``len(docs)``).
        This can be passed in to avoid recomputing the size of docs if that might
        be expensive (i.e., a QuerySet which would require an extra DB call).

    * *format_type*: The format to render into. Options are ``xml``.

    **Returns:** 

    * an HTTPResponse whose body is an XML string containing the rendered list of 
        documents (which might be empty).

    """

    if docs:
        for doc in docs:
            if doc.id:
                _set_doc_latest(doc)
                doc.relates_to, doc.is_related_from = _get_doc_relations(doc)

    return utils.render_template('documents', {  'docs'      : docs, 
                                                                                             'record'    : record, 
                                                                                             'pha'       : pha, 
                                                                                             'tdc'       : tdc}, 
                                                                                                type=format_type)

def _get_document(record=None, carenet=None, document_id=None, pha=None, external_id=None):
    """ Fetch a document from the DB.
    
    EITHER *document_id* OR *external_id* must be provided (exclusive or). If a 
    document doesn't exist matching all passed arguments, this call returns None.

    **Arguments:**
    
    * *record*: if the document is record-specific, this
        :py:class:`~indivo.models.records_and_documents.Record`
        instance refers to the document's record.

    * *carenet*: if the document is being found via a carenet, this
        :py:class:`~indivo.models.share.Carenet`
        instance refers to the carenet containing the document. 

        .. warning::

             Carenet membership is NOT checked in this function. That security
             must be checked elsewhere.

    * *document_id*: the internal identifier for the document, if available.

        .. note::
             
             One of *external_id* or *document_id* MUST be passed to this function,
             or it cannot retrieve a unique document.

    * *pha*: if the document is application-specific, this
        :py:class:`~indivo.models.apps.PHA` instance refers to the 
        application to which the document pertains.

    * *external_id*: the external identifier for the document, if available. The
        identifier should already have been prepared using
        :py:meth:`~indivo.models.records_and_documents.Document.prepare_external_id`.
     
        .. note::
             
             One of *external_id* or *document_id* MUST be passed to this function,
             or it cannot retrieve a unique document.

    **Returns:**

    * An instance of 
        :py:class:`~indivo.models.records_and_documents.Document`,
        on success.

    * None, if a document satisfying all passed arguments could not be found.

    """
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

def __local_document_create(request, record, pha, external_id, existing_doc):
    """ Create a document, or update one in place.

    This function serves 
    :py:meth:`~indivo.views.documents.document.document_create` and 
    :py:meth:`~indivo.views.documents.document.document_create_or_update`,
    which encompasses record- and/or app-specific documents.

    The external_id is expected to be already adjusted.

    **Arguments:**

    * *request*: The incoming Django HttpRequest object.

    * *record*: if the document is record-specific, this
        :py:class:`~indivo.models.records_and_documents.Record`
        instance refers to the document's record.

    * *pha*: if the document is application-specific, this
        :py:class:`~indivo.models.apps.PHA` instance refers to the 
        application to which the document pertains.  

    * *external_id*: the external identifier to assing to the new document, 
        if available. The identifier should already have been prepared using
        :py:meth:`~indivo.models.records_and_documents.Document.prepare_external_id`.

    * *existing_doc*: If the new document will overwrite (via in-place update
        or versioning) an existing document, this 
        :py:class:`~indivo.models.records_and_documents.Document`
        instance references the old document to be overwritten.

    **Returns:**

    * An HttpResponse object whose body is a string of XML describing the created 
        document, ready for return over the wire on success.

    * An instance of :py:class:`django.http.HttpResponseBadRequest` if the new
        document failed validation during the creation process.

    **Raises:**
    
    * :py:exc:`django.db.IntegrityError`: if the arguments to this function
        violate a database unique constraint (i.e., duplicate external id).

        .. warning::

             If an :py:exc:`IntegrityError` is raised, it will invalidate the 
             current database transaction. Calling functions should handle this
             case and rollback the current transaction.

    """

    try:
        doc = _document_create(record             = record, 
                               creator           = request.principal,
                               pha               = pha, 
                               content           = request.raw_post_data, 
                               external_id       = external_id,
                               replaces_document = existing_doc,
                               mime_type         = utils.get_content_type(request))
    except ValueError, e:
        return HttpResponseBadRequest("the document submitted is malformed:" + str(e))

    _set_doc_latest(doc)
    return utils.render_template('document', {'record': doc.record, 
                                            'doc'     : doc, 
                                            'pha'     : pha }) 


@commit_on_200
def document_create(request, record):
    """ Create a record-specific Indivo Document.

    Calls into 
    :py:meth:`~indivo.views.documents.document.__local_document_create`.

    """

    return __local_document_create(request, record, pha=None,
                                   external_id = None, existing_doc=None)

@commit_on_200
@handle_integrity_error('Duplicate external id. Each document requires a unique external id')
def document_create_by_ext_id(request, record, pha, external_id):
    """ Create a record-specific Indivo Document with an associated external id.

    Calls into 
    :py:meth:`~indivo.views.documents.document.__local_document_create`.

    """
    return  __local_document_create(request, record, pha=None,
                                                     external_id=Document.prepare_external_id(external_id, pha),
                                                     existing_doc=None)

@commit_on_200
def app_document_create_or_update(request, pha, document_id):
    """ Create or Overwrite an app-specific Indivo document.

    Calls into
    :py:meth:`~indivo.views.documents.document.document_create_or_update`.

    """

    return document_create_or_update(request, pha=pha, document_id=document_id)

@commit_on_200
def app_document_create(request, pha):
    """ Create an app-specific Indivo document.

    Calls into
    :py:meth:`~indivo.views.documents.document.document_create_or_update`.

    """

    return document_create_or_update(request, pha=pha)

@commit_on_200
def app_document_create_or_update_ext(request, pha, external_id):
    """ Create an app-specific Indivo document with an associated external id.

    Calls into
    :py:meth:`~indivo.views.documents.document.document_create_or_update`.

    """

    return document_create_or_update(request, pha, external_id=external_id)

@commit_on_200
def record_app_document_create(request, record, pha):
    """ Create a record-app-specific Indivo document.

    Calls into
    :py:meth:`~indivo.views.documents.document.document_create_or_update`.

    """

    return document_create_or_update(request, pha, record=record)

@commit_on_200
def record_app_document_create_or_update_ext(request, record, pha, external_id):
    """ Create or Overwrite a record-app-specific Indivo document with an associated external id.

    Calls into
    :py:meth:`~indivo.views.documents.document.document_create_or_update`.

    """
    return document_create_or_update(request, pha, record=record, external_id=external_id)

def document_create_or_update(request, pha, record=None, document_id=None, external_id=None):
    """ Create or Overwrite an app-specific or record-app-specific document, possibly with an associated external id.

    Prepares the external id, loads the existing document to overwrite, then
    calls into 
    :py:meth:`~indivo.views.documents.document.__local_document_create`.

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
    """ Retrieve a record-app-specific document. 
    
    Calls into :py:meth:`~indivo.views.documents.document.document`.

    """
    return document(request, document_id, record=record, pha=pha)


def app_specific_document(request, pha, document_id):
    """ Retrive an app-specific document.

    Calls into :py:meth:`~indivo.views.documents.document.document`.

    """

    return document(request, document_id, pha=pha)


def record_specific_document(request, record, document_id):
    """ Retrieve a record-specific document.

    Calls into :py:meth:`~indivo.views.documents.document.document`.

    """

    return document(request, document_id, record=record)

def document(request, document_id, record=None, pha=None):
    """ Retrieve a document, record- and/or app-specific. 

    **Arguments:**

    * *request*: the incoming Django HttpRequest object.

    * *document_id*: the internal identifier of the document to retrieve.

    * *record*: if the document is record-specific, this
        :py:class:`~indivo.models.records_and_documents.Record`
        instance refers to the document's record.

    * *pha*: if the document is application-specific, this
        :py:class:`~indivo.models.apps.PHA` instance refers to the 
        application to which the document pertains.  

    **Returns:**

    * An HttpResponse object whose body contains the raw content of the document 
        on success.

    **Raises:**
    
    * A :py:exc:`django.http.Http404` if the document could not be found.

    """

    document = _get_document(pha=pha, record=record, document_id=document_id)
    if not document \
        or (pha and document.pha != pha):
        raise Http404
    
    return _render_document(document)

def _render_document(document):
    """ Get the raw content of a document, ready to be sent over the wire.

    **Arguments:**

    * *document*: the
        :py:class:`~indivo.models.records_and_documents.Document`
        instance to render.
        
    **Returns:**

    * An HttpResponse object whose body contains the The raw content of the 
        document on success.

    """

    # no content, must be a file
    if not document.content:
        return HttpResponse(document.content_file, mimetype=document.mime_type)

    return HttpResponse(document.content, mimetype="application/xml")


@marsloader()
def app_document_list(request, pha, limit, offset, status, order_by='created_at'):
    """ List app-specific documents.

    Calls into :py:meth:`~indivo.views.documents.document.document_list`.

    """

    return document_list(request, limit, offset, status, order_by, pha=pha)

@marsloader()
def record_document_list(request, record, limit, offset, status, order_by='created_at'):
    """ List record-specific documents.

    Calls into :py:meth:`~indivo.views.documents.document.document_list`.

    """

    return document_list(request, limit, offset, status, order_by, record=record)

@marsloader()
def record_app_document_list(request, record, pha, limit, offset, status, order_by='created_at'):
    """ List record-app-specific documents.

    Calls into :py:meth:`~indivo.views.documents.document.document_list`.

    """

    return document_list(request, limit, offset, status, order_by, record=record, pha=pha)

def document_list(request, limit, offset, status, order_by='created_at', record=None, pha=None):
    """ List Indivo documents.

    **Arguments:**

    * *request*: The incoming Django HttpRequest object. ``request.GET`` may contain:
    
        * *type*: The Indivo document schema type on which to filter the resut set. As 
            of 2010-08-16, type is no longer part of the URL, it's only in the GET
            query parameters.


    * *limit*, *offset*, *status*, *order_by*: Standard paging and filtering 
        arguments. See :py:func:`~indivo.lib.view_decorators.marsloader`
        or :doc:`/query-api`.

    * *record*: if desired documents are record-specific, this
        :py:class:`~indivo.models.records_and_documents.Record`
        instance refers to the record to filter on.

    * *pha*: if the desired documents are application-specific, this
        :py:class:`~indivo.models.apps.PHA` instance refers to the 
        app to filter on.

    **Returns:**

    * an HTTPResponse whose body is an XML string containing the rendered list of 
        documents (which might be empty), on success.

    **Raises:**
    
    * :py:exc:`django.http.Http404`: if *type* was passed, but didn't 
        correspond to an existing Indivo schema.

    """

    fqn = DocumentProcessing.expand_schema(request.GET.get('type', None))
    try:
        if fqn:
            try:
                if record:
                    docs = record.documents.filter(fqn=fqn, 
                                                   replaced_by=None, status=status, pha=pha).order_by(order_by)
                else:
                    docs = Document.objects.filter(fqn=fqn, 
                                                   pha=pha, replaced_by=None, status=status).order_by(order_by)
                return _render_documents(docs, record, pha, docs.count())
            except DocumentSchema.DoesNotExist:
                raise Http404
        docs = Document.objects.filter(record=record, 
                                       replaced_by=None, pha=pha, status=status).order_by(order_by)
    except:
        docs = []
    return _render_documents(docs[offset:offset+limit], record, pha, len(docs))

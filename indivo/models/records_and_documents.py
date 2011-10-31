"""
Indivo Model for records and documents
"""
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile

import urllib, hashlib, uuid

from base import Object, Principal, BaseModel, INDIVO_APP_LABEL
from accounts import Account
from shares import AccountFullShare, PHAShare, Carenet
from messaging import Message
from notifications import Notification
from status import StatusName, DocumentStatusHistory
from oauth import oauth

## Indivo Records and Documents
class Record(Object):
  # owner (could be the hospital if the person does not own their own record)
  owner = models.ForeignKey('Principal', related_name = 'records_owned_by', null=True)

  # label that the owner uses
  label = models.CharField(max_length=60, null = True)

  # for lightweight distributed transaction control
  # nullable for those who don't want to consider it
  external_id = models.CharField(max_length = 250, null = True, unique=True)

  # basic demographic information, this will be XML or possibly RDF

  @classmethod
  def prepare_external_id(cls, local_external_id, principal_email):
    """
    This utility method creates a 'full' external_id from parameters
    """
    if not local_external_id:
      return None

    return "%s/%s" % (principal_email, local_external_id)

  def __unicode__(self):
    return 'Record %s' % self.id

  def can_admin(self, account):
    return (self.owner == account) or AccountFullShare.objects.filter(record = self, with_account = account)

  @property
  def phas(self):
    # addeed a filter for those shares that are not pha shares
    return [s.with_pha for s in self.pha_shares.all()]

  def has_pha(self, pha):
    # look for token
    try:
      tok = PHAShare.objects.filter(record = self, with_pha = pha)
    except PHAShare.DoesNotExist:
      return False

    return len(tok) > 0

  def get_accounts_to_notify(self):
    """A list of notification routes
    
    Includes a default for the owner of the record
    """

    accounts = list(set([r.account for r in self.notification_routes.all()]))
    if self.owner and (self.owner not in accounts):
      try:
        owner_account = Account.objects.get(email = self.owner.email)
        accounts.append(owner_account)
      except Account.DoesNotExist:
        pass
    return accounts

  def get_messages(self):
    return Message.objects.filter(about_record = self)

  def send_message(self, external_identifier, sender, subject, body, body_type='plaintext', num_attachments = 0, severity='low'):
    # FIXME: does the PHA have the right to notify the account?
    # FIXME: is the routing really the same for notifications and messages
    # go through all of the accounts that need to be notified
    for account in self.get_accounts_to_notify():
      # FIXME: does the account have the right to see notifications on this record?

      #account.notify_account_of_new_message()
      Message.objects.create( account             = account, 
                              about_record        = self, 
                              external_identifier = external_identifier,
                              sender              = sender, 
                              recipient           = account, 
                              subject             = subject,
                              body                = body,
                              body_type           = body_type,
                              num_attachments     = num_attachments,
                              severity            = severity)


  contact = models.ForeignKey('Document', related_name='the_record_for_contact', null=True)
  demographics = models.ForeignKey('Document', related_name='the_record_for_demographics', null=True)

  def notify(self, pha, content, document_id=None, app_url=None):
    # make sure that the document belongs to the record
    document = None
    if document_id:
      document = Document.objects.get(id = document_id)
      if document.record != self:
        raise PermissionDenied()

    # go through all of the accounts that need to be notified
    for account in self.get_accounts_to_notify():
      Notification.objects.create(record    = self, 
                                  sender    = pha, 
                                  account   = account, 
                                  content   = content, 
                                  creator   = pha, 
                                  document  = document, 
                                  app_url   = app_url)

  @transaction.commit_on_success
  def create_default_carenets(self):
    for carenet_name in settings.INDIVO_DEFAULT_CARENETS:
      cn = Carenet.objects.get_or_create(name = carenet_name, record = self)

  @property
  def carenet_alias_id(self):
    """
    eventually, a real carenet alias will be created, but for now it's
    the record ID, since it's all UUIDs
    """
    return self.id

class DocumentSchema(Object):
  type = models.CharField(max_length = 500)
  stylesheet = models.ForeignKey('Document', null=True, related_name='stylesheet')
  internal_p = models.BooleanField(default=True)
  
  CONTACTS = None

  DEFAULT_REL_NAMESPACE = 'http://indivo.org/vocab/documentrels#'

  @classmethod
  def expand_rel(cls, rel):
    if rel is None:
      return None

    if rel.find(':') > -1 or rel.find('/') > -1:
      return rel
    else:
      return "%s%s" % (cls.DEFAULT_REL_NAMESPACE, rel)
    
  @classmethod
  def setup(cls):
    try:
      cls.CONTACTS = cls.objects.get(type='Contacts')
    except:
      # SZ: What makes this call special?  Why not do a try/except rollback for all calls, if not, why for this one?
      # Because we 'know' it should be there?
      from django.db import transaction
      try:
        transaction.rollback()
      except:
        pass

  @property
  def uri(self):
    return self.type

  # how does this schema map to simple user-level categories
  # allergy, immunization, lab, surgery, condition, medication
  
  # how this is transformed to RDF (pointer to XSLT)

class Document(Object):
  # SZ: We don't want both record AND pha to both be null
  # SZ: We need to add an integrity check for this... 
  record = models.ForeignKey(Record, related_name='documents', null=True)

  # for lightweight distributed transaction control
  # nullable for those who don't want to consider it
  # this external_id may be formatted as one of the following:
  # - {pha_email}/{pha_local_external_id}
  # - {pha_email}/INTERNAL/{pha_local_external_id}
  # - {pha_email}/NORECORD/{pha_local_external_id}

  # you might think (as Ben did), that this is a useful case:
  # - {record_level_external_id}
  # but it's not. external_ids are always scoped to app.
  external_id = models.CharField(max_length = 250, null = True)

  # a parameter to indicate that a document should never be shared,
  # no matter what. If it is true, then it is never accessible except
  # within the record
  nevershare = models.BooleanField(default=False, null=False)

  @classmethod
  def prepare_external_id(cls, local_external_id, pha, pha_specific=False, record_specific=True):
    """
    This utility method creates a 'full' external_id from parameters depending
    on app specificity and record specifity of the document.

    Eventually, abstracting this within the Document model would be ideal
    """
    if not local_external_id:
      return None

    if not pha:
      raise ValueError("an external ID must be scoped to a PHA, cannot prepare an external ID without a PHA")

    if not pha_specific and not record_specific:
      raise ValueError("requested an external ID with a document neither record-specific nor pha_specific")

    if not record_specific:
      return "%s/NORECORD/%s" % (pha.email, local_external_id)

    if pha_specific:
      return "%s/INTERNAL/%s" % (pha.email, local_external_id)
    else:
      return "%s/%s" % (pha.email, local_external_id)


  #type = models.URLField()
  # xml type
  type = models.ForeignKey(DocumentSchema, null = True)

  # mime type
  mime_type = models.CharField(max_length=100, null = True)

  # this might be XMLField eventually
  content = models.TextField(null=True)

  # if it's binary, then it's stored as a file
  # the use of the date is just to prevent too many documents in a single directory
  # eventually this might be done using a storage manager that looks at the UUID and 
  # does even partitioning, rather than just date.
  content_file = models.FileField(upload_to='indivo_documents/%Y/%m/%d')

  # PHA specific document?
  pha = models.ForeignKey('PHA', null=True, related_name = 'pha_document')

  suppressed_at = models.DateTimeField(null=True, blank=True)
  suppressed_by = models.ForeignKey('Principal', null=True)
  original = models.ForeignKey('self', related_name='document_thread', null=True)
  replaced_by = models.ForeignKey('self', related_name='document_replaced', null=True)
  replaces = models.ForeignKey('self', null=True)

  size = models.IntegerField()
  label = models.CharField(max_length=100, null=True)
  digest = models.CharField(max_length=64, null=False)
  status = models.ForeignKey('StatusName', null=False, default=1)

  #related_docs = models.ManyToManyField('self', through='DocumentRels', symmetrical=False)

  # Ben says: I would like this to be pre-computed if possible, probably at insertion time
  def latest(self, id, created_at, creator_email):
    self.latest_id            = id
    self.latest_created_at    = created_at
    self.latest_creator_email = creator_email

  def set_status(self, principal, status, reason):

    # For more explanation on proxied_by_email and effective_principal_email
    # Please see middlewares/audit.py
    effective_principal_email = principal.effective_principal.email

    if principal.proxied_by:
      proxied_by_email = principal.proxied_by.email
    else:
      proxied_by_email = None

    if status and reason:
      status_name = StatusName.objects.get(name=status)
      self.status = status_name
      self.save()

    # Everytime set_status is called we'll record it in DocumentStatusHistory
    # The status and reason is the new status and new reason
    # not the old status and old reason
    # of the given doc which is 'self'

    # Save document status history
    DocumentStatusHistory.objects.create( document              = self.id,
                                          record                = self.record.id,
                                          status                = status_name,
                                          reason                = reason,
                                          proxied_by_principal  = proxied_by_email,
                                          effective_principal   = effective_principal_email)


  #tags = models.ManyToManyField(RecordTag, null = True, blank=True)

  # [ben] not sure why I can't do Meta = BaseMeta, but I can't
  class Meta:
    app_label = INDIVO_APP_LABEL

    # 2010-08-15 changed to just record and external_id.
    # for non-record pha documents, we are not properly preventing duplication
    # but that's how it has to be for now.
    unique_together = (('record', 'external_id'),)

  def __unicode__(self):
    return "Document %s" % self.id


  # 1/2/2011: Moving Document Processing into the model - DH
  def replace(self, new_content, new_mime_type):
    """
    Replace the content of the current document with new content and mime_type
    """
    if self.replaced_by:
      raise ValueError("cannot replace a document that is already replaced")

    from indivo.document_processing.document_processing import DocumentProcessing
    new_doc = DocumentProcessing(new_content, new_mime_type)
    if not new_doc.is_binary:
      # set content and mime_type
      self.content = new_doc.content
      self.mime_type = new_mime_type
      
      # empty out derived fields so that doc processing will repopulate them
      self.type = None
      self.size = None
      self.digest = None

    else:
      # Why aren't we doing anything for binaries?
      pass

    self.processed = False # We have changed the content, which now needs processing
    self.save()
    return True

  processed = models.BooleanField(default=False)

  def save(self, *args, **kwargs):
    """
    Handle document processing whenever a new document is created. This method
    processes the document, updates fact objects, and then saves the document
    """
    if self.processed:
      doc = None # Nothing to do here

    else:
      # import dynamically because DocumentProcessing imports DocumentSchema from this file
      from indivo.document_processing.document_processing import DocumentProcessing
      doc = DocumentProcessing(self.content, self.mime_type)

      # Process the Doc, if necessary
      if not self.pha and self.content:
        doc.process()

      # Delete fact objects from the document we are replacing
      if self.replaces:
        from indivo.models import Fact
        Fact.objects.filter(document = self.replaces).delete()

      # Update document info based on processing
      if doc.is_binary:
        self.content = None
      self.type = self.type if self.type else doc.get_document_schema()
      self.size = self.size if self.size else doc.get_document_size()
      self.digest = self.digest if self.digest else doc.get_document_digest()

      # Mark document as processed
      self.processed = True

    # Oracle is incompatible with multi-column unique constraints where
    # one column might be null (i.e., UNIQUE(record, external_id)).
    # We therefore insure that all Documents have an external id,
    # mirroring the internal id if none was passed in.
  
    # Set the external_id to a random uuid so that we can save it to the
    # db before it has an internal id
    if not self.external_id:
      self.external_id = 'TEMP-EXTID' + str(uuid.uuid4())

    super(Document,self).save(*args, **kwargs)

    # Do we need to rewrite this to the DB after changes?
    save_again = False

    # If we set a temporary external_id, set it to mirror the internal id
    if self.external_id.startswith('TEMP-EXTID'):
      self.external_id = self.id
      save_again = True

    # Update newly created Fact objs, if we created any
    if doc and hasattr(doc, 'f_objs'):
      for fobj in doc.f_objs:
        if fobj:
          fobj.document = self
          fobj.record = self.record
          fobj.save()

    if not self.original:
      self.original = self
      save_again = True

    if save_again:
      self.save()

DocumentSchema.setup()

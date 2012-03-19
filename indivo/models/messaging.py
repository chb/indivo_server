"""
Indivo Model for Messaging
"""

from django.db import models
from django.conf import settings

from base import Object, Principal, INDIVO_APP_LABEL

class Message(Object):
    account = models.ForeignKey('Account')

    # about which record is this message?
    about_record = models.ForeignKey('Record', null = True)

    # identifier that can be set by sender
    external_identifier = models.CharField(max_length = 250, null = True)
    sender = models.ForeignKey('Principal', related_name = 'message_as_sender')
    recipient = models.ForeignKey('Principal', related_name = 'message_as_recipient')
    
    SEVERITIES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'))

    # content of message
    severity = models.CharField(max_length=100, default="low", choices=SEVERITIES)
    subject = models.CharField(max_length = 100)

    BODY_TYPES = (
        ('plaintext', 'Plain Text'),
        ('markdown', 'MarkDown')
        )

    # type of the body
    body_type = models.CharField(max_length = 100, default="plaintext", choices=BODY_TYPES)

    body = models.TextField()
    
    received_at = models.DateTimeField(auto_now_add = True)
    read_at = models.DateTimeField(auto_now_add=False, null=True)
    archived_at = models.DateTimeField(auto_now_add=False, null=True)

    # if the user responds to this message
    response_to = models.ForeignKey('self', null=True, related_name='message_responses')

    num_attachments = models.IntegerField(default = 0)

    class Meta:
        app_label = INDIVO_APP_LABEL
        unique_together = (('account', 'external_identifier', 'sender'),)

    @property
    def ready(self):
        return self.messageattachment_set.count() == self.num_attachments
    
    def add_attachment(self, attachment_num, content):
        """
        attachment_num is 1-indexed
        """

        if int(attachment_num) > self.num_attachments:
            raise Exception("attachment num is too high")
        
        mime_type='application/xml' # Only handle XML attachments for now

        from indivo.document_processing.document_processing import DocumentProcessing
        doc_utils = DocumentProcessing(content, mime_type)

        attachment = MessageAttachment.objects.create(
            message = self,
            content = content,
            size = doc_utils.size,
            type = doc_utils.fqn,
            attachment_num = attachment_num)

        return attachment

    def get_attachment(self, attachment_num):
        return MessageAttachment.objects.get(message=self, attachment_num = attachment_num)

class MessageAttachment(Object):
    """
    for now supports only XML attachments
    """

    message = models.ForeignKey(Message)
    
    # bytes
    size = models.IntegerField()

    # xml type
    type = models.CharField(max_length = 250)

    content = models.TextField()

    saved_to_document = models.ForeignKey('Document', null=True)

    attachment_num = models.IntegerField()

    class Meta:
        app_label = INDIVO_APP_LABEL
        unique_together = (('message', 'attachment_num'),)

    @property
    def saved(self):
        return self.saved_to_document != None

    def save_as_document(self, account):
        """
        The account is the one who's doing the saving

        FIXME: need to check the external_id situation, which could cause problems if senders don't use it well.
        """
        if self.saved:
            raise Exception("this attachment already saved to record")
        
        record = self.message.about_record
        if record == None:
            raise Exception("can only save attachments that pertain to a record")

        external_id = "SAVED_ATTACHMENT_%s_%s" % (self.message.external_identifier , str(self.attachment_num))

        # FIXME: this import shows that we should move the _document_create function to models from views.
        from indivo.views.documents.document import _document_create
        self.saved_to_document = _document_create(creator = account, content = self.content,
                                                  pha = None, record = record, external_id = external_id,
                                                  mime_type = 'application/xml')
        self.save()
                                                  

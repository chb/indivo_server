from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.models import MessageAttachment, Fact
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.message import TEST_MESSAGES, TEST_ATTACHMENTS
from indivo.tests.data.account import TEST_ACCOUNTS

from django.db import IntegrityError, transaction

class MessageAttachmentModelUnitTests(InternalTests):
    def setUp(self):
        super(MessageAttachmentModelUnitTests, self).setUp()
    
        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        
        # A Message
        self.message = self.createMessage(TEST_MESSAGES, 3, about_record=self.record, recipient=self.account)

        # An attachment
        self.attachment = self.createAttachment(TEST_ATTACHMENTS, 1, message=self.message)
        
    def tearDown(self):
        super(MessageAttachmentModelUnitTests, self).tearDown()
     
    @enable_transactions
    def test_construction(self):

        # Should be able to construct normally
        try:
            ma = self.createAttachment(TEST_ATTACHMENTS, 0)
        except:
            self.fail('Unable to construct message attachment with standard args')
        else:
            self.assertEqual(ma, MessageAttachment.objects.get(pk=ma.pk))

        # Should not be able to construct without a message
        try:
            ma2 = self.createAttachment(TEST_ATTACHMENTS, 0, force_create=True, message=None)
        except:
            transaction.rollback()
        else:
            self.fail('Constructed a message attachment with no message')

    def test_save_as_document(self):
        
        # expected state
        self.assertFalse(self.attachment.saved)
        n_fobjs = Fact.objects.all().count()

        # save the attachment
        self.attachment.save_as_document(self.account)
        
        self.assertTrue(self.attachment.saved)
        self.assertEqual(self.attachment.content, self.attachment.saved_to_document.content)
        self.assertNotEqual(n_fobjs, Fact.objects.all().count()) # doc should have been processed, creating a fact
        self.assertEqual(self.attachment.type, self.attachment.saved_to_document.fqn)
        self.assertEqual(self.attachment.size, self.attachment.saved_to_document.size)
        self.assertEqual(self.attachment.saved_to_document.external_id, 
                         'SAVED_ATTACHMENT_%s_%s'%(self.attachment.message.external_identifier, 
                                                   self.attachment.attachment_num))

        # Try to resave: expect failure
        self.assertRaises(Exception, self.attachment.save_as_document, self.account)
        
        # Try to save to no record: expect failure
        self.attachment.message.about_record = None
        self.attachment.saved_to_document = None
        self.assertRaises(Exception, self.attachment.save_as_document, self.account)

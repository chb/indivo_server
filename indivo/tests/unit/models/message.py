from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.models import MessageAttachment, Message
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.message import TEST_MESSAGES, TEST_ATTACHMENTS
from indivo.tests.data.account import TEST_ACCOUNTS

from django.db import IntegrityError, transaction

class MessageModelUnitTests(InternalTests):
    def setUp(self):
        super(MessageModelUnitTests, self).setUp()
    
        # A recipient account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A sender app
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # A record, owned by the recipient account
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        
        # A Message, sent by the sender app to the recipient account about the record
        self.message = self.createMessage(TEST_MESSAGES, 3, sender=self.app,
                                          account=self.account, about_record=self.record, recipient=self.account)

        # An attachment for the message
        self.attachment = self.createAttachment(TEST_ATTACHMENTS, 1, message=self.message)
        
    def tearDown(self):
        super(MessageModelUnitTests, self).tearDown()
     
    @enable_transactions
    def test_construction(self):

        # Should be able to construct normally
        try:
            m = self.createMessage(TEST_MESSAGES, 0)
        except:
            self.fail('Unable to construct message with standard args')
        else:
            self.assertEqual(m, Message.objects.get(pk=m.pk))

        # Should not be able to violate unique constraint (identical account, external_id, sender)
        try:
            m = self.createMessage(TEST_MESSAGES, 0, force_create=True)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Constructed a message attachment with no message')

        # Should not be able to construct without a sender or recipient
        try:
            m = self.createMessage(TEST_MESSAGES, 0, force_create=True, sender=None)
        except ValueError:
            pass
        else:
            self.fail('Constructed a message with no sender')

        try:
            m = self.createMessage(TEST_MESSAGES, 0, force_create=True, recipient=None)
        except ValueError:
            pass
        else:
            self.fail('Constructed a message with no recipient')

    def test_ready(self):

        # The message we created had all one of its attachments, it should be ready
        self.assertTrue(self.message.ready)

        # Let's take away the attachment
        self.attachment.delete()
        self.assertFalse(self.message.ready)

    @enable_transactions
    def test_add_attachment(self):
        
        # Let's take away our attachment
        self.attachment.delete()

        # And add it back
        attachment = self.message.add_attachment(self.attachment.attachment_num, self.attachment.content)

        self.assertTrue(self.message.ready)
        self.assertEqual(attachment.message, self.message)
        self.assertEqual(attachment.content, self.attachment.content)
        self.assertEqual(attachment.size, self.attachment.size)
        self.assertEqual(attachment.type, self.attachment.type)
        self.assertEqual(attachment.attachment_num, self.attachment.attachment_num)

        # Shouldn't work with a bad attachment number
        self.assertRaises(Exception, self.message.add_attachment, 
                          self.attachment.attachment_num+1, self.attachment.content)

        # Shouldn't work twice
        try:
            self.message.add_attachment(self.attachment.attachment_num, self.attachment.content)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Added two attachments to the same slot')


    def test_get_attachment(self):
        
        # get our attachment
        attachment = self.message.get_attachment(self.attachment.attachment_num)
        
        self.assertEqual(attachment.message, self.message)
        self.assertEqual(attachment.content, self.attachment.content)
        self.assertEqual(attachment.size, self.attachment.size)
        self.assertEqual(attachment.type, self.attachment.type)
        self.assertEqual(attachment.attachment_num, self.attachment.attachment_num)

        # fail to get some crazy-numbered attachments
        self.assertRaises(MessageAttachment.DoesNotExist, self.message.get_attachment, -30)
        self.assertRaises(MessageAttachment.DoesNotExist, self.message.get_attachment, 50)
        self.assertRaises(MessageAttachment.DoesNotExist, self.message.get_attachment, 0)
        self.assertRaises(MessageAttachment.DoesNotExist, self.message.get_attachment,
                          self.attachment.attachment_num+1)

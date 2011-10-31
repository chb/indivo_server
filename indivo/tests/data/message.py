from indivo.models import Message, MessageAttachment
from indivo.document_processing.document_processing import DocumentProcessing
from base import *
from reports.allergy import TEST_ALLERGIES

class TestMessage(TestModel):
    model_fields = ['sender', 'recipient', 'external_identifier', 'account', 'about_record',
                    'severity', 'subject', 'body_type', 'body', 'num_attachments']
    model_class = Message
    
    def _setupargs(self, body='NO BODY', sender=None, recipient=None, message_id=None, account=None, about_record=None,
                   severity='low', subject='NO SUBJECT', body_type='plaintext', num_attachments=0):
        self.sender=sender
        self.recipient=recipient
        self.external_identifier = message_id
        self.account=account
        self.about_record=about_record
        self.severity=severity
        self.subject=subject
        self.body_type=body_type,
        self.body = body
        self.num_attachments = num_attachments

class TestMessageAttachment(TestModel):
    model_fields = ['message', 'attachment_num', 'content', 'size', 'type']
    model_class = MessageAttachment
    
    def _setupargs(self, attachment_num=1, message=None, content='<?xml version="1.0" ?><body></body>', 
                   size=None, type=None):
        self.message = message
        self.attachment_num = attachment_num
        self.content = content
        self.size = size or len(content)
        self.type = type or DocumentProcessing(content, 'application/xml').xml_type

_TEST_MESSAGES = [
    {'subject':'test 1', 
     'body':'hello world', 
     'message_id':'msg_01', 
     'severity':'medium',
     'account': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'sender': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'recipient': ForeignKey('account', 'TEST_ACCOUNTS', 1),
     'about_record': ForeignKey('record', 'TEST_RECORDS', 0),
     },
    {'subject':'test 2', 
     'body':'hello mars', 
     'message_id':'msg_02', 
     'severity':'high',
     'account': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'sender': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'recipient': ForeignKey('account', 'TEST_ACCOUNTS', 1),
     'about_record': ForeignKey('record', 'TEST_RECORDS', 0),
     },
    {'subject':'subj',
     'body':'message_body',
     'message_id':'msg_id',
     'body_type':'plaintext',
     'severity':'low',
     'num_attachments':1,
     'account': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'sender': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'recipient': ForeignKey('account', 'TEST_ACCOUNTS', 1),
     'about_record': ForeignKey('record', 'TEST_RECORDS', 0),
     },
    {'subject':'subj2',
     'body':'message_body2',
     'message_id':'msg_id2',
     'body_type':'plaintext',
     'severity':'low',
     'num_attachments':1,
     'account': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'sender': ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'recipient': ForeignKey('account', 'TEST_ACCOUNTS', 1),
     'about_record': ForeignKey('record', 'TEST_RECORDS', 0),
     },
    ]
TEST_MESSAGES = scope(_TEST_MESSAGES, TestMessage)

_TEST_ATTACHMENTS = [
    {'message': ForeignKey('message', 'TEST_MESSAGES', 2),
     'attachment_num': 1,
     'content':'<?xml version="1.0" ?><body></body>',
     'size':len('<?xml version="1.0" ?><body></body>'),
     'type':'body'
     },
    {'message': ForeignKey('message', 'TEST_MESSAGES', 3),
     'attachment_num': 1,
     'content': TEST_ALLERGIES[0]['content'],
     'size':len(TEST_ALLERGIES[0]['content']),
     'type':'http://indivo.org/vocab/xml/documents#Allergy',
     },
    ]
TEST_ATTACHMENTS = scope(_TEST_ATTACHMENTS, TestMessageAttachment)

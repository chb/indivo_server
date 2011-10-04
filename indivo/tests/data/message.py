from indivo.models import Message, MessageAttachment
from indivo.models.messaging import DocParser
from base import TestModel, raw_data_to_objs, ForeignKey

class TestMessage(TestModel):
    model_fields = ['sender', 'recipient', 'external_identifier', 'account', 'about_record',
                    'severity', 'subject', 'body_type', 'body', 'num_attachments']
    model_class = Message
    
    def __init__(self, body='NO BODY', sender=None, recipient=None, message_id=None, account=None, about_record=None,
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
    
    def __init__(self, attachment_num=1, message=None, content='<?xml version="1.0" ?><body></body>', 
                 size=None, type=None):
        self.message = message
        self.attachment_num = attachment_num
        self.content = content
        self.size = size or len(content)
        self.type = type or DocParser(content).xml_type

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
    ]

_TEST_ATTACHMENTS = [
    {'message': ForeignKey('message', 'TEST_MESSAGES', 2),
     'attachment_num': 1,
     'content':'<?xml version="1.0" ?><body></body>',
     },
    ]

TEST_MESSAGES = raw_data_to_objs(_TEST_MESSAGES, TestMessage)
TEST_ATTACHMENTS = raw_data_to_objs(_TEST_ATTACHMENTS, TestMessageAttachment)

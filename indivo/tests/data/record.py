from indivo.models import Record
from base import *

class TestRecord(TestModel):
    model_fields = ['label', 'contact', 'demographics', 'owner', 'external_id']
    model_class = Record

    def _setupargs(self, label, contact=None, demographics=None, owner=None, external_id=None, extid_principal_key=None):
        self.label = label
        self.contact = contact
        self.demographics = demographics
        self.owner = owner
        self.local_external_id = external_id
        if extid_principal_key:
            self.external_id = Record.prepare_external_id(external_id, extid_principal_key.to.raw_data['account_id'])
        else:
            self.external_id = None
        

_TEST_RECORDS = [
    {'label':'testing_record_label',
     'contact':ForeignKey('document', 'TEST_CONTACTS', 0),
     'demographics':ForeignKey('document', 'TEST_DEMOGRAPHICS', 0),
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'test_record_label2',
     'contact':ForeignKey('document', 'TEST_CONTACTS', 0),
     'demographics':ForeignKey('document', 'TEST_DEMOGRAPHICS', 0),
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'empty_record',
     },
    {'label':'bob',
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'jane',
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'test_record_extid',
     'contact':ForeignKey('document', 'TEST_CONTACTS', 1),
     'demographics':ForeignKey('document', 'TEST_DEMOGRAPHICS', 0),
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'external_id':'RECORD5_EXTID',
     'extid_principal_key':ForeignKey('account', 'TEST_ACCOUNTS', 4),
     },

]
TEST_RECORDS = scope(_TEST_RECORDS, TestRecord)

from indivo.models import Record
from base import TestModel, raw_data_to_objs, ForeignKey

class TestRecord(TestModel):
    model_fields = ['label', 'contact', 'demographics', 'owner', 'external_id']
    model_class = Record

    def __init__(self, label, contact=None, demographics=None, owner=None, external_id=None, extid_principal=None):
        self.label = label
        self.contact = contact
        self.demographics = demographics
        self.owner = owner
        self.local_external_id = external_id
        if extid_principal:
            self.external_id = Record.prepare_external_id(external_id, extid_principal.email)
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
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'bob',
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'jane',
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'test_record_extid',
     'contact':ForeignKey('document', 'TEST_CONTACTS', 0),
     'demographics':ForeignKey('document', 'TEST_DEMOGRAPHICS', 0),
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'extid_principal':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },

]

TEST_RECORDS = raw_data_to_objs(_TEST_RECORDS, TestRecord)

from indivo.models import Record, Demographics
from base import *

class TestRecord(TestModel):
    model_fields = ['label', 'demographics', 'owner', 'external_id']
    model_class = Record

    def _setupargs(self, label, demographics=None, owner=None, external_id=None, extid_principal_key=None):
        self.label = label
        self.demographics = demographics
        self.owner = owner
        self.local_external_id = external_id
        if extid_principal_key:
            self.external_id = Record.prepare_external_id(external_id, extid_principal_key.to.raw_data['account_id'])
        else:
            self.external_id = None

_TEST_RECORDS = [
    {'label':'testing_record_label',
     'demographics':ForeignKey('demographics', 'TEST_DEMOGRAPHICS', 0),
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     },
    {'label':'test_record_label2',
     'demographics':ForeignKey('demographics', 'TEST_DEMOGRAPHICS', 1),
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
     'demographics':ForeignKey('demographics', 'TEST_DEMOGRAPHICS', 2),
     'owner':ForeignKey('account', 'TEST_ACCOUNTS', 0),
     'external_id':'RECORD5_EXTID',
     'extid_principal_key':ForeignKey('account', 'TEST_ACCOUNTS', 4),
     },

]
TEST_RECORDS = scope(_TEST_RECORDS, TestRecord)

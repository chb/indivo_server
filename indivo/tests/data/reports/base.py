from indivo.tests.data.base import ForeignKey, raw_data_to_objs
from indivo.tests.data.document import TestDocument

def report_content_to_test_docs(content_list):
    default_args = {'label':'rdoc1',
                    'record':ForeignKey('record', 'TEST_RECORDS', 0),
                    'creator':ForeignKey('account','TEST_ACCOUNTS',0),
                    }
    raw_data = [dict(default_args, content=c) for c in content_list]
    return raw_data_to_objs(raw_data, TestDocument)

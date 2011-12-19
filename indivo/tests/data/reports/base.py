from indivo.tests.data.base import *
from indivo.tests.data.document import TestDocument

def report_content_to_test_docs(content_list):
    default_args = {'label':'report_doc',
                    'record':ForeignKey('record', 'TEST_RECORDS', 0),
                    'creator':ForeignKey('account','TEST_ACCOUNTS',0),
                    }
    raw_data = [dict(default_args, content=c) for c in content_list]
    raw_data = scope(raw_data, TestDocument)
    return raw_data

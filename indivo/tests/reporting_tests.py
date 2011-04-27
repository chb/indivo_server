from indivo.models import *
from internal_tests import InternalTests
from django.utils.http import urlencode
import hashlib, uuid

from indivo.tests.data import *

EMAIL, FULLNAME, CONTACT_EMAIL, USERNAME, PASSWORD, RECORDS = ("mymail@mail.ma","full name","contact@con.con","user","pass",("the mom", "the dad", "the son", "the daughter"))

DOCUMENT = '''<DOC>HERE'S MY CONTENT</DOC>'''
DOC_LABEL = 'A Document!'

class ReportingInternalTests(InternalTests):
    accounts = []
    records = []
    carenets = []
    labs = []

    def setUp(self):
        super(ReportingInternalTests,self).setUp()

        # reset our state
        self.accounts = []
        self.records = []
        self.carenets = []
        self.labs = []

        # Create an Account (with a few records)
        acct_args = {'email':EMAIL, 'full_name':FULLNAME, 'contact_email':CONTACT_EMAIL}
        self.accounts.append(self.createAccount(USERNAME, PASSWORD, RECORDS, **acct_args))

        # Track the records and carenets we just created
        for record in Record.objects.all():
            self.records.append(record)
        for carenet in Carenet.objects.all():
            self.carenets.append(carenet)

        #Add some sample Labs
        self.labs = self.loadTestLabs(self.records[0], self.accounts[0])

    def tearDown(self):
        super(ReportingInternalTests,self).tearDown()

    def test_get_labs(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/labs/?group_by=lab_type&aggregate_by=count*lab_test_name&date_range=date_measured*2010-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        # should see {['lab_type': u'1,25-Dihydroxy Vitamin D', 'aggregation': 1}]
        print 'RESPONSE 1: ', response.content

        url2 = '/records/%s/reports/minimal/labs/?lab_type=hematology&date_group=date_measured*month&aggregate_by=count*lab_type&order_by=date_measured&date_range=date_measured*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        # Should see [{'aggregation': 1, u'month': u'1998-07'}, {'aggregation': 1, u'month': u'2009-07'}]
        print 'RESPONSE 2: ', response.content

        url3 = '/records/%s/reports/minimal/labs/?lab_type=hematology&order_by=date_measured&date_range=date_measured*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url3)
        # should see 1 lab from 2009-07
        print 'RESPONSE 3: ', response.content

        url4 = '/records/%s/reports/minimal/labs/?lab_type=hematology&order_by=date_measured&date_range=date_measured*1995-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url4)
        # should see 2 labs now, first from 1998, second from 2009-07
        print 'RESPONSE 4: ', response.content

#        url5 = '/records/%s/reports/minimal/labs/?order_by=date_measured&date_range=date_measured*1995-03-10T00:00:00Z*&lab_test_value='%(record_id)
#        response = self.client.get(url4)
#        # should see 2 labs now, first from 1998, second from 2009-07
#        print 'RESPONSE 4: ', response.content

        #CHECK RESULTS MORE CAREFULLY

    def test_get_audits(self):
        record_id = self.records[0].id        

        # make some audits
        import datetime
        audit_args = {
            'datetime': datetime.datetime.now(),
            'view_func': 'FUNC1',
            'request_successful': True,
            'record_id': record_id
            }
        Audit.objects.create(**audit_args)
        audit_args = {
            'datetime': datetime.datetime.now(),
            'view_func': 'FUNC2',
            'request_successful': True, 
            'record_id': record_id
            }
        Audit.objects.create(**audit_args)


        url = '/records/%s/audits/query/?date_range=request_date*2010-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        # Should see 2 entries
        print 'RESPONSE 1: ', response.content

        url = '/records/%s/audits/query/?date_range=request_date*2010-03-10T00:00:00Z*&function_name=FUNC1'%(record_id)
        response = self.client.get(url)
        # Should see 1 entry
        print 'RESPONSE 2: ', response.content

        url = '/records/%s/audits/query/?aggregate_by=count*request_date&date_range=request_date*2010-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        # Should see [{'aggregation': 4}]
        print 'RESPONSE 3: ', response.content

        url = '/records/%s/audits/query/?aggregate_by=count*request_date&date_range=request_date*2010-03-10T00:00:00Z*&function_name=FUNC1'%(record_id)
        response = self.client.get(url)
        # Should see [{'aggregation': 1}]
        print 'RESPONSE 4: ', response.content

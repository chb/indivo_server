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

        #Add some sample Reports
        self.loadTestReports(self.records[0], self.accounts[0])
        self.labs = list(Lab.objects.all())

    def tearDown(self):
        super(ReportingInternalTests,self).tearDown()

    # TODO: ADD BETTER TESTS OF RESPONSE DATA, NOT JUST 200s

    def test_get_vitals(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/vitals/?group_by=category&aggregate_by=min*value&date_range=date_measured*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/vitals/weight%%20test/?category=Blood%%20Pressure%%20Systolic&date_group=date_measured*month&aggregate_by=sum*value&order_by=date_measured'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/vitals/?order_by=-created_at&date_measured=2009-05-16T15:23:21Z'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_simple_clinical_notes(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/simple-clinical-notes/?group_by=specialty&aggregate_by=count*provider_name&date_range=date_of_visit*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/simple-clinical-notes/?provider_name=Kenneth%%20Mandl&date_group=date_of_visit*month&aggregate_by=count*provider_name&order_by=date_of_visit'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/simple-clinical-notes/?order_by=-created_at'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_procedures(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/procedures/?group_by=procedure_name&aggregate_by=count*procedure_name&date_range=date_performed*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/procedures/?procedure_name=Appendectomy&date_group=date_performed*month&aggregate_by=count*procedure_name&order_by=-date_performed'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/procedures/?order_by=date_performed'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_problems(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/problems/?group_by=problem_name&aggregate_by=count*problem_name&date_range=date_onset*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/problems/?problem_name=Myocardial%%20Infarction&date_group=date_onset*month&aggregate_by=count*problem_name&order_by=-date_onset'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/problems/?order_by=date_onset'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_medications(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/medications/?group_by=medication_brand_name&aggregate_by=count*medication_name&date_range=date_started*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/medications/?medication_brand_name=Vioxx&date_group=date_started*month&aggregate_by=count*medication_name&order_by=-date_started&date_range=date_started*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/medications/?order_by=date_started&date_range=date_started*2009-02-17T03:00:00.02Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_measurements(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/measurements/HBA1C/?group_by=lab_code&aggregate_by=avg*value&date_range=date_measured*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/measurements/HBA1C/?lab_code=HBA1C&date_group=date_measured*month&aggregate_by=max*value&order_by=date_measured&date_range=date_measured*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/measurements/HBA1C/?order_by=date_measured&date_range=date_measured*2009-06-17T03:00:00.02Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_immunizations(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/immunizations/?group_by=vaccine_type&aggregate_by=count*date_administered&date_range=date_administered*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/immunizations/?vaccine_type=Hepatitis%%20B&date_group=date_administered*month&aggregate_by=count*vaccine_type&order_by=date_administered&date_range=date_administered*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/immunizations/?vaccine_type=adenovirus%%20vaccine,%%20NOS&order_by=date_administered&date_range=date_administered*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_labs(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/labs/?group_by=lab_type&aggregate_by=count*lab_test_name&date_range=date_measured*2010-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # should see {['lab_type': u'1,25-Dihydroxy Vitamin D', 'aggregation': 1}]

        url2 = '/records/%s/reports/minimal/labs/?lab_type=hematology&date_group=date_measured*month&aggregate_by=count*lab_type&order_by=date_measured&date_range=date_measured*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)
        # Should see [{'aggregation': 1, u'month': u'1998-07'}, {'aggregation': 1, u'month': u'2009-07'}]

        url3 = '/records/%s/reports/minimal/labs/?lab_type=hematology&order_by=date_measured&date_range=date_measured*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)
        # should see 1 lab from 2009-07

        url4 = '/records/%s/reports/minimal/labs/?lab_type=hematology&order_by=date_measured&date_range=date_measured*1995-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url4)
        self.assertEquals(response.status_code, 200)
        # should see 2 labs now, first from 1998, second from 2009-07

    def test_get_allergies(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/allergies/?group_by=allergen_type&aggregate_by=count*allergen_name&date_range=date_diagnosed*2004-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/allergies/?allergen_type=Drugs&date_group=date_diagnosed*month&aggregate_by=count*allergen_type&order_by=date_diagnosed&date_range=date_diagnosed*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/allergies/?allergen_type=Drugs&order_by=date_diagnosed&date_range=date_diagnosed*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_equipment(self):
        record_id = self.records[0].id
        url = '/records/%s/reports/minimal/equipment/?group_by=equipment_vendor&aggregate_by=count*equipment_name&date_range=date_started*2004-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/equipment/?equipment_name=Tractor&date_group=date_started*month&aggregate_by=count*equipment_name&order_by=date_started&date_range=date_started*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/equipment/?order_by=date_started&date_range=date_started*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

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
        self.assertEquals(response.status_code, 200)

        url = '/records/%s/audits/query/?date_range=request_date*2010-03-10T00:00:00Z*&function_name=FUNC1'%(record_id)
        response = self.client.get(url)
        # Should see 1 entry
        self.assertEquals(response.status_code, 200)

        url = '/records/%s/audits/query/?aggregate_by=count*request_date&date_range=request_date*2010-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        # Should see [{'aggregation': 4}]
        self.assertEquals(response.status_code, 200)

        url = '/records/%s/audits/query/?aggregate_by=count*request_date&date_range=request_date*2010-03-10T00:00:00Z*&function_name=FUNC1'%(record_id)
        response = self.client.get(url)
        # Should see [{'aggregation': 1}]
        self.assertEquals(response.status_code, 200)

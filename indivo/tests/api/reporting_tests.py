from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data import *

import json
from lxml import etree

DOCUMENT = '''<DOC>HERE'S MY CONTENT</DOC>'''
DOC_LABEL = 'A Document!'
NS = 'http://indivo.org/vocab/xml/documents#'

class ReportingInternalTests(InternalTests):

    def setUp(self):
        super(ReportingInternalTests,self).setUp()

        # Create an Account (with a few records)
        self.account = self.createAccount(TEST_ACCOUNTS, 4)

        # Add a record for it
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)

        #Add some sample Reports
        self.loadTestReports(record=self.record)

    def tearDown(self):
        super(ReportingInternalTests,self).tearDown()

    # TODO: ADD BETTER TESTS OF RESPONSE DATA, NOT JUST 200s

    def test_get_vitals(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/vitals/?group_by=category&aggregate_by=min*value&date_range=date_measured*2005-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/vitals/weight%%20test/?category=Blood%%20Pressure%%20Systolic&date_group=date_measured*month&aggregate_by=sum*value&order_by=date_measured'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/vitals/?order_by=-created_at&date_measured=2009-05-16T15:23:21Z'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)
        
        # find by specific value
        url = '/records/%s/reports/minimal/vitals/?value=185.0'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Check values
        xml = etree.XML(response.content)
        reports = xml.findall('.//{%s}VitalSign' % NS)
        self.assertEqual(len(reports), 1)
        
        for report in reports:
            vital_value = report.findtext('.//{%s}value' % NS)
            self.assertEquals(float(vital_value), 185)
        
        # find by specific values
        url = '/records/%s/reports/minimal/vitals/?value=185.0|145'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Check values
        xml = etree.fromstring(response.content)
        reports = xml.findall('.//{%s}VitalSign' % NS)
        self.assertEqual(len(reports), 2)
        
        for report in reports:
            vital_value = report.findtext('.//{%s}value' % NS)
            self.assertTrue(float(vital_value) in [185, 145])

    def test_get_simple_clinical_notes(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/simple-clinical-notes/?group_by=specialty&aggregate_by=count*provider_name&date_range=date_of_visit*2005-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/simple-clinical-notes/?provider_name=Kenneth%%20Mandl&date_group=date_of_visit*month&aggregate_by=count*provider_name&order_by=date_of_visit'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/simple-clinical-notes/?order_by=-created_at'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_procedures(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/procedures/?group_by=procedure_name&aggregate_by=count*procedure_name&date_range=date_performed*2005-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/procedures/?procedure_name=Appendectomy&date_group=date_performed*month&aggregate_by=count*procedure_name&order_by=-date_performed'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/procedures/?order_by=date_performed'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)


    def test_get_measurements(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/measurements/HBA1C/?group_by=lab_code&aggregate_by=avg*value&date_range=date_measured*2005-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/measurements/HBA1C/?lab_code=HBA1C&date_group=date_measured*month&aggregate_by=max*value&order_by=date_measured&date_range=date_measured*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/measurements/HBA1C/?order_by=date_measured&date_range=date_measured*2009-06-17T03:00:00.02Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)
        
    def test_get_immunizations(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/immunizations/?group_by=vaccine_type&aggregate_by=count*date_administered&date_range=date_administered*2005-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/immunizations/?vaccine_type=Hepatitis%%20B&date_group=date_administered*month&aggregate_by=count*vaccine_type&order_by=date_administered&date_range=date_administered*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/immunizations/?vaccine_type=adenovirus%%20vaccine,%%20NOS&order_by=date_administered&date_range=date_administered*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_labs(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/labs/?group_by=lab_type&aggregate_by=count*lab_test_name&date_range=date_measured*2010-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)
        
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # should see {['lab_type': u'1,25-Dihydroxy Vitamin D', 'aggregation': 1}]
        # check result size
        xml = etree.XML(response.content)
        reports = xml.findall('.//{%s}AggregateReport' % NS)
        self.assertEqual(len(reports), 1)
        # check aggregate results
        self.assertEqual(reports[0].get('value'), '1')
        self.assertEqual(reports[0].get('group'), '1,25-Dihydroxy Vitamin D')

        url = '/records/%s/reports/minimal/labs/?lab_type=hematology&date_group=date_measured*month&aggregate_by=count*lab_type&order_by=date_measured&date_range=date_measured*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Should see [{'aggregation': 1, u'month': u'1998-07'}, {'aggregation': 1, u'month': u'2009-07'}]
        # check result size
        xml = etree.XML(response.content)
        reports = xml.findall('.//{%s}AggregateReport' % NS)
        self.assertEqual(len(reports), 2)
        # check aggregate results
        self.assertEqual(reports[0].get('value'), '1')
        self.assertEqual(reports[0].get('group'), '1998-07')
        self.assertEqual(reports[1].get('value'), '1')
        self.assertEqual(reports[1].get('group'), '2009-07')

        url = '/records/%s/reports/minimal/labs/?lab_type=hematology&order_by=date_measured&date_range=date_measured*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # should see 1 lab from 2009-07
        # check result size
        xml = etree.fromstring(response.content)
        reports = xml.findall('.//{%s}LabReport' % NS)
        self.assertEqual(len(reports), 1)
        # make sure results fall within our date_range
        min_date = self.validateIso8601('2000-03-10T00:00:00Z')
        for report in reports:
            date_measured = report.findtext('.//{%s}dateMeasured' % NS)
            date_measured = self.validateIso8601(date_measured)
            self.assertTrue(date_measured >= min_date)

        url = '/records/%s/reports/minimal/labs/?lab_type=hematology&order_by=date_measured&date_range=date_measured*1995-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # check result size
        xml = etree.fromstring(response.content)
        reports = xml.findall('.//{%s}LabReport' % NS)
        self.assertEqual(len(reports), 2)
        # make sure results fall within our date_range
        min_date = self.validateIso8601('1995-03-10T00:00:00Z')
        for report in reports:
            date_measured = report.findtext('.//{%s}dateMeasured' % NS)
            date_measured = self.validateIso8601(date_measured)
            self.assertTrue(date_measured >= min_date)
        
        url = '/records/%s/reports/minimal/labs/?lab_type=hematology|1,25-Dihydroxy Vitamin D'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Ensure that we retrieved 3 labs of the correct lab_type
        xml = etree.fromstring(response.content)
        reports = xml.findall('.//{%s}LabReport' % NS)
        self.assertEqual(len(reports), 3)
        
        for report in reports:
            lab_type = report.findtext('.//{%s}labType' % NS)
            self.assertTrue(lab_type in ['hematology', '1,25-Dihydroxy Vitamin D'])
            
        url = '/records/%s/reports/minimal/labs/?lab_type=hematology|nonexistentlabtype'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Ensure that we retrieved 2 labs of the correct lab_type
        xml = etree.fromstring(response.content)
        reports = xml.findall('.//{%s}LabReport' % NS)
        self.assertEqual(len(reports), 2)
        
        for report in reports:
            lab_type = report.findtext('.//{%s}labType' % NS)
            self.assertTrue(lab_type in ['hematology', 'nonexistentlabtype'])
            
        url = '/records/%s/reports/minimal/labs/?lab_type=nonexistentlabtype1|nonexistentlabtype2|nonexistentlabtype3'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Ensure that we retrieved 0 labs
        xml = etree.fromstring(response.content)
        reports = xml.findall('.//{%s}LabReport' % NS)
        self.assertEqual(len(reports), 0)
        
        # find by specific dates
        url = '/records/%s/reports/minimal/labs/?date_measured=2010-07-16T12:00:00Z|1998-07-16T12:00:00Z'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Ensure that we retrieved 1 lab with the correct date_measured
        xml = etree.fromstring(response.content)
        reports = xml.findall('.//{%s}LabReport' % NS)
        self.assertEqual(len(reports), 1)
        
        for report in reports:
            lab_type = report.findtext('.//{%s}dateMeasured' % NS)
            self.assertTrue(lab_type in ['2010-07-16T12:00:00Z', '1998-07-16T12:00:00Z'])

    def test_get_equipment(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/equipment/?group_by=equipment_vendor&aggregate_by=count*equipment_name&date_range=date_started*2004-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/minimal/equipment/?equipment_name=Tractor&date_group=date_started*month&aggregate_by=count*equipment_name&order_by=date_started&date_range=date_started*1990-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/minimal/equipment/?order_by=date_started&date_range=date_started*2000-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_audits(self):
        record_id = self.record.id        

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
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)
        
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

    def test_get_generic_labs(self):
        response = self.client.get('/records/%s/reports/Lab/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        
        response_json = json.loads(response.content)
        self.assertTrue(len(response_json), 4)

        # check to make sure Model name is correct, and that it has 14 fields        
        first_lab = response_json[0]
        self.assertEquals(first_lab['__modelname__'], 'Lab')
        self.assertEquals(len(first_lab), 14)

    def test_generic_query_api(self):
        record_id = self.record.id
        #TODO: Vitals is currently the only data model with a numeric field to aggregate on, 
        #      and there are only 2 of them; making meaningful queries difficult.
        
        # group_by, aggregate_by, date_range (json format)
        url = '/records/%s/reports/vitals/?group_by=name&aggregate_by=min*value&date_range=date_measured*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Check aggregate report
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)      
        self.assertEqual(response_json[0]['__modelname__'], 'AggregateReport')
        self.assertTrue(float(response_json[0]['value']) in [185, 145])
        self.assertTrue(response_json[0]['group'] in ['weight test', 'Blood Pressure Systolic'])
        self.assertTrue(float(response_json[1]['value']) in [185, 145])

        # group_by, aggregate_by, date_range (xml format)
        url = '/records/%s/reports/vitals/?group_by=name&aggregate_by=min*value&date_range=date_measured*2005-03-10T00:00:00Z*&response_format=application/xml'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        xml = etree.XML(response.content)
        reports = xml.findall('.//AggregateReport')
        self.assertEqual(len(reports), 2)
        # check aggregate results
        self.assertTrue(float(reports[0].get('value')) in [185, 145])
        self.assertTrue(reports[0].get('group') in ['Blood Pressure Systolic', 'weight test'])

        # string {field}, date_group, aggregate_by, order_by
        url = '/records/%s/reports/vitals/?date_group=date_measured*month&aggregate_by=sum*value&order_by=date_measured'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Check aggregate report
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)      
        self.assertEqual(response_json[0]['__modelname__'], 'AggregateReport')
        self.assertTrue(float(response_json[0]['value']) in [185, 145])
        self.assertEqual(response_json[0]['group'], '2009-05')
        self.assertEqual(response_json[1]['__modelname__'], 'AggregateReport')
        self.assertTrue(float(response_json[1]['value']) in [185, 145])
        self.assertEqual(response_json[1]['group'], '2009-05')
        
        # date {field}
        url = '/records/%s/reports/vitals/?date_measured=2009-05-16T15:23:21Z'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)      
        self.assertEqual(response_json[0]['date_measured'], '2009-05-16T15:23:21Z')
        self.assertEqual(response_json[1]['date_measured'], '2009-05-16T15:23:21Z')
        
        # string {field}
        url = '/records/%s/reports/vitals/?name=weight test'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)      
        self.assertEqual(response_json[0]['name'], 'weight test')
        
        # number {field}
        url = '/records/%s/reports/vitals/?value=185.0'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Check values
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        
        self.assertEquals(float(response_json[0]['value']), 185)
        
        # number {field} with multiple values
        url = '/records/%s/reports/vitals/?value=185.0|145'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Check values
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)
        
        for vital in response_json:
            self.assertTrue(float(vital['value']) in [185, 145])


    def test_get_generic_nonexistent(self):  
        # get a JSON encoded report on a non-existent model
        response = self.client.get('/records/%s/reports/DoesNotExist/'%(self.record.id), {'response_format':'application/json'})
        self.assertEquals(response.status_code, 404)

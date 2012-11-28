import json
from lxml import etree

from rdflib import Graph, Namespace

from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data import TEST_ACCOUNTS, TEST_RECORDS

DOCUMENT = '''<DOC>HERE'S MY CONTENT</DOC>'''
DOC_LABEL = 'A Document!'
NS = 'http://indivo.org/vocab/xml/documents#'
SMART = Namespace("http://smartplatforms.org/terms#")

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

    def test_get_simple_clinical_notes(self):
        record_id = self.record.id
        url = '/records/%s/reports/ClinicalNote/'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/ClinicalNote/?provider_name_family=Mandel'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/ClinicalNote/?order_by=-created_at'%(record_id)
        response = self.client.get(url3)
        self.assertEquals(response.status_code, 200)

    def test_get_procedures(self):
        record_id = self.record.id
        url = '/records/%s/reports/procedure/?group_by=name_code_title&aggregate_by=count*name_code_title&date_range=date*2005-03-10T00:00:00Z*'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url2 = '/records/%s/reports/procedure/?name_code_title=Appendectomy&date_group=date*month&aggregate_by=count*name_code_title&order_by=-date'%(record_id)
        response = self.client.get(url2)
        self.assertEquals(response.status_code, 200)

        url3 = '/records/%s/reports/procedure/?order_by=date'%(record_id)
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
        response = self.client.get('/records/%s/reports/LabResult/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        
        response_json = json.loads(response.content)
        self.assertTrue(len(response_json), 1)

        # check to make sure Model name is correct, and that it has 37 fields        
        first_lab = response_json[0]
        self.assertEquals(first_lab['__modelname__'], 'LabResult')
        self.assertEquals(len(first_lab), 43)

    def test_generic_query_api(self):
        record_id = self.record.id
        #TODO: Vitals is currently the only data model with a numeric field to aggregate on, 
        #      and there are only 2 of them; making meaningful queries difficult.
        
        # group_by, aggregate_by, date_range (json format)
        url = '/records/%s/reports/vitalsigns/?group_by=weight_unit&aggregate_by=avg*weight_value&date_range=date*2005-03-10T00:00:00Z*'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Check aggregate report
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)      
        self.assertEqual(response_json[0]['__modelname__'], 'AggregateReport')
        self.assertEqual(float(response_json[0]['value']), 75.8)
        self.assertEqual(response_json[0]['group'], 'kg')

        # group_by, aggregate_by, date_range (xml format)
        url = '/records/%s/reports/vitalsigns/?group_by=weight_unit&aggregate_by=avg*weight_value&date_range=date*2005-03-10T00:00:00Z*&response_format=application/xml'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        xml = etree.XML(response.content)
        reports = xml.findall('.//AggregateReport')
        self.assertEqual(len(reports), 1)
        # check aggregate results
        self.assertEqual(float(reports[0].get('value')), 75.8)
        self.assertEqual(reports[0].get('group'), 'kg')

        # string {field}, date_group, aggregate_by, order_by
        url = '/records/%s/reports/vitalsigns/?date_group=date*month&aggregate_by=min*date&order_by=date'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Check aggregate report
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)      
        self.assertEqual(response_json[0]['__modelname__'], 'AggregateReport')
        self.assertEqual(response_json[0]['value'], '2009-05-16T12:00:00Z')
        self.assertEqual(response_json[0]['group'], '2009-05')
        self.assertEqual(response_json[1]['__modelname__'], 'AggregateReport')
        self.assertEqual(response_json[1]['value'], '2010-05-16T12:00:00Z')
        self.assertEqual(response_json[1]['group'], '2010-05')
        
        # date {field}
        url = '/records/%s/reports/vitalsigns/?date=2009-05-16T12:00:00Z'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)      
        self.assertEqual(response_json[0]['date'], '2009-05-16T12:00:00Z')
        
        # string {field}
        url = '/records/%s/reports/vitalsigns/?weight_name_code_title=Body weight'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)      
        self.assertEqual(response_json[0]['weight_name_code_title'], 'Body weight')
        self.assertEqual(response_json[1]['weight_name_code_title'], 'Body weight')
        
        # number {field}
        url = '/records/%s/reports/vitalsigns/?weight_value=70.8'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        # Check values
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEquals(float(response_json[0]['weight_value']), 70.8)
        
        # number {field} with multiple values
        url = '/records/%s/reports/vitalsigns/?weight_value=70.8|80.8'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Check values
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)
        for vital in response_json:
            self.assertTrue(float(vital['weight_value']) in [70.8, 80.8])

    def test_get_generic_nonexistent(self):  
        # get a JSON encoded report on a non-existent model
        response = self.client.get('/records/%s/reports/DoesNotExist/'%(self.record.id), {'response_format':'application/json'})
        self.assertEquals(response.status_code, 404)

    def test_get_smart_problems(self):
        response = self.client.get('/records/%s/problems/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        self.assertEqual(len(problems), 1)
        
        # retrieve a single problem
        problem_id = problems[0].split('/')[-1]
        
        response = self.client.get('/records/%s/problems/%s' % (self.record.id, problem_id))
        self.assertEquals(response.status_code, 200)
        g.parse(data=response.content, format="application/rdf+xml")
        encounters = [e for e in g.subjects(None,SMART["Encounter"])]
        self.assertEqual(len(encounters), 2)

    def test_get_smart_labs(self):
        response = self.client.get('/records/%s/lab_results/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 1)
        
        # retrieve a single lab result
        lab_id = lab_results[0].split('/')[-1]
        
        response = self.client.get('/records/%s/lab_results/%s' % (self.record.id, lab_id))
        self.assertEquals(response.status_code, 200)
        
        # grab labs with specific LOINC code
        response = self.client.get('/records/%s/lab_results/?loinc=2951-2'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 1)
        
        # grab labs with bad LOINC code
        response = self.client.get('/records/%s/lab_results/?loinc=2951-2fake'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 0)
        
        # grab labs with date_from
        response = self.client.get('/records/%s/lab_results/?date_from=2009-05-16'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 1)
        
        # grab labs with date_from
        response = self.client.get('/records/%s/lab_results/?date_from=2009-05-17'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 0)
        
        # grab labs with date_to
        response = self.client.get('/records/%s/lab_results/?date_to=2009-05-15'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 0)
        
        # grab labs with date_to
        response = self.client.get('/records/%s/lab_results/?date_to=2009-05-16'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 1)
        
    def test_get_smart_allergies(self):
        # allergies are a special case since they can be an Allergy or AllergyExclusion 
        response = self.client.get('/records/%s/allergies/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        allergy_results = [a for a in g.subjects(None,SMART["Allergy"])]
        self.assertEqual(len(allergy_results), 1)
        allergy_exclusion_results = [a for a in g.subjects(None,SMART["AllergyExclusion"])]
        self.assertEqual(len(allergy_exclusion_results), 0)
        
        # retrieve a single allergy
        allergy_id = allergy_results[0].split('/')[-1]
        
        response = self.client.get('/records/%s/allergies/%s' % (self.record.id, allergy_id))
        self.assertEquals(response.status_code, 200)        

    def test_get_smart_procedures(self):
        response = self.client.get('/records/%s/procedures/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        procedures = [p for p in g.subjects(None,SMART["Procedure"])]
        self.assertEqual(len(procedures), 2)

        # retrieve a single procedure
        procedure_id = procedures[0].split('/')[-1]
        
        response = self.client.get('/records/%s/procedures/%s' % (self.record.id, procedure_id))
        self.assertEquals(response.status_code, 200)
        
    def test_get_smart_social_history(self):
        response = self.client.get('/records/%s/social_history/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        histories = [h for h in g.subjects(None,SMART["SocialHistory"])]
        self.assertEqual(len(histories), 1)

        # retrieve a single procedure
        history_id = histories[0].split('/')[-1]
        
        response = self.client.get('/records/%s/social_history/%s' % (self.record.id, history_id))
        self.assertEquals(response.status_code, 200)
        
    def test_get_smart_clinical_note(self):
        response = self.client.get('/records/%s/clinical_notes/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        notes = [n for n in g.subjects(None,SMART["ClinicalNote"])]
        self.assertEqual(len(notes), 1)

        # retrieve a single procedure
        note_id = notes[0].split('/')[-1]
        
        response = self.client.get('/records/%s/clinical_notes/%s' % (self.record.id, note_id))
        self.assertEquals(response.status_code, 200)
        
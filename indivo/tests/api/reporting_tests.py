import json
from lxml import etree

from rdflib import Graph, Namespace
from rdflib.collection import Collection

from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data import TEST_ACCOUNTS, TEST_RECORDS

DOCUMENT = '''<DOC>HERE'S MY CONTENT</DOC>'''
DOC_LABEL = 'A Document!'
NS = 'http://indivo.org/vocab/xml/documents#'
SMART = Namespace("http://smartplatforms.org/terms#")
SPAPI = Namespace("http://smartplatforms.org/terms/api#")

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

    def test_get_vital_signs(self):
        url = '/records/%s/reports/vitalsigns/?group_by=weight_unit&aggregate_by=avg*weight_value'%(self.record.id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        url = '/records/%s/reports/vitalsigns/?aggregate_by=avg*weight_value'%(self.record.id)
        response = self.client.get(url)
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
        self.assertEqual(len(problems), 7)
        
        # retrieve a single problem
        problem_id = problems[0].split('/')[-1]
        
        response = self.client.get('/records/%s/problems/%s' % (self.record.id, problem_id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        self.assertEqual(len(problems), 1)

    def test_get_smart_lab_panels(self):
        response = self.client.get('/records/%s/lab_panels/'%(self.record.id))
        self.assertEquals(response.status_code, 200)

        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_panels = [l for l in g.subjects(None,SMART["LabPanel"])]
        self.assertEqual(len(lab_panels), 1)
    
    def test_get_smart_lab_results(self):
        response = self.client.get('/records/%s/lab_results/'%(self.record.id))
        self.assertEquals(response.status_code, 200)

        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 2)
        
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
        self.assertEqual(len(lab_results), 2)
        
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
        self.assertEqual(len(lab_results), 2)
        
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
        response = self.client.get('/records/%s/lab_results/?date_to=2009-05-16T23:59:59Z'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        lab_results = [l for l in g.subjects(None,SMART["LabResult"])]
        self.assertEqual(len(lab_results), 2)
        
    def test_get_smart_allergies(self):
        # allergies are a special case since they can be an Allergy or AllergyExclusion 
        response = self.client.get('/records/%s/allergies/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        allergy_results = [a for a in g.subjects(None,SMART["Allergy"])]
        self.assertEqual(len(allergy_results), 2)
        allergy_exclusion_results = [a for a in g.subjects(None,SMART["AllergyExclusion"])]
        self.assertEqual(len(allergy_exclusion_results), 1)
        
        # retrieve a single allergy
        allergy_id = allergy_results[0].split('/')[-1]
        
        response = self.client.get('/records/%s/allergies/%s' % (self.record.id, allergy_id))
        self.assertEquals(response.status_code, 200)        
        
        # test paging (currently allergies are ordered by date created
        response = self.client.get('/records/%s/allergies/?limit=2' % (self.record.id))
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        allergy_results = [a for a in g.subjects(None,SMART["Allergy"])]
        self.assertEqual(len(allergy_results), 2)
        allergy_exclusion_results = [a for a in g.subjects(None,SMART["AllergyExclusion"])]
        self.assertEqual(len(allergy_exclusion_results), 0)
        # grab the next page
        next_page_url = [a for a in g.objects(None, SPAPI['nextPageURL'])][0]
        response = self.client.get(next_page_url)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        allergy_results = [a for a in g.subjects(None,SMART["Allergy"])]
        self.assertEqual(len(allergy_results), 0)
        allergy_exclusion_results = [a for a in g.subjects(None,SMART["AllergyExclusion"])]
        self.assertEqual(len(allergy_exclusion_results), 1)

    def test_get_smart_encounters(self):
        response = self.client.get('/records/%s/encounters/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        encounters = [e for e in g.subjects(None,SMART["Encounter"])]
        self.assertEqual(len(encounters), 4)

        # retrieve a single encounter
        encounter_id = encounters[0].split('/')[-1]
        
        response = self.client.get('/records/%s/encounters/%s' % (self.record.id, encounter_id))
        self.assertEquals(response.status_code, 200)
        
    def test_get_smart_immunizations(self):
        response = self.client.get('/records/%s/immunizations/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        immunizations = [i for i in g.subjects(None,SMART["Immunization"])]
        self.assertEqual(len(immunizations), 1)

        # retrieve a single immunization
        immunization_id = immunizations[0].split('/')[-1]
        
        response = self.client.get('/records/%s/immunizations/%s' % (self.record.id, immunization_id))
        self.assertEquals(response.status_code, 200)

    def test_get_smart_medications(self):
        response = self.client.get('/records/%s/medications/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        medications = [m for m in g.subjects(None,SMART["Medication"])]
        self.assertEqual(len(medications), 1)

        # retrieve a single medication
        medication_id = medications[0].split('/')[-1]
        
        response = self.client.get('/records/%s/medications/%s' % (self.record.id, medication_id))
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
        
    def test_get_smart_vitals(self):
        response = self.client.get('/records/%s/vital_sign_sets/'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        vitals = [v for v in g.subjects(None,SMART["VitalSignSet"])]
        self.assertEqual(len(vitals), 2)

        # retrieve a single vital sign set
        vital_sign_set_id = vitals[0].split('/')[-1]
        
        response = self.client.get('/records/%s/vital_sign_sets/%s' % (self.record.id, vital_sign_set_id))
        self.assertEquals(response.status_code, 200)
        
    def test_smart_limit_and_offset(self):
        # limit to 5
        response = self.client.get('/records/%s/problems/?limit=5'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        self.assertEqual(len(problems), 5)

        # limit to 5 and offset from 5
        response = self.client.get('/records/%s/problems/?limit=5&offset=5'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        self.assertEqual(len(problems), 2)

        # offset past the end
        response = self.client.get('/records/%s/problems/?limit=5&offset=8'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        self.assertEqual(len(problems), 0)

        # negative offset should translate to offset of 0
        response = self.client.get('/records/%s/problems/?limit=5&offset=-1'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        self.assertEqual(len(problems), 5)
        
        # non-integer offset should return 400
        response = self.client.get('/records/%s/problems/?limit=5&offset=a'%(self.record.id))
        self.assertEquals(response.status_code, 400)
        
    def test_smart_response_summary(self):
        # response summary for paged results
        response = self.client.get('/records/%s/problems/?limit=5'%(self.record.id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")

        response_summary = [s for s in g.subjects(None,SPAPI['ResponseSummary'])]
        self.assertEqual(len(response_summary), 1, "expected a single ResponseSummary")
        response_summary = response_summary[0]
        next_page_url = [a for a in g.objects(response_summary, SPAPI['nextPageURL'])][0]
        results_returned = [a for a in g.objects(response_summary, SPAPI['resultsReturned'])][0]
        self.assertEqual(results_returned, 5, "expected resultsReturned to be 5")
        total_result_count = [a for a in g.objects(response_summary, SPAPI['totalResultCount'])][0]
        self.assertEqual(total_result_count, 7, "expected totalResultCount to be 7")
        result_order = [a for a in g.objects(response_summary, SPAPI['resultOrder'])][0]
        problem_list = list(Collection(g, result_order))
        self.assertEqual(len(problem_list), 5, "wrong length for resultOrder")
        
        # grab the nextPageURL from previous request
        response = self.client.get(next_page_url)
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        self.assertEqual(len(problems), 2)
        
        # response summary for single instance
        problems = [p for p in g.subjects(None,SMART["Problem"])]
        problem_id = problems[0].split('/')[-1]
        
        response = self.client.get('/records/%s/problems/%s' % (self.record.id, problem_id))
        self.assertEquals(response.status_code, 200)
        g = Graph()
        g.parse(data=response.content, format="application/rdf+xml")
        response_summary = [s for s in g.subjects(None,SPAPI['ResponseSummary'])]
        self.assertEqual(len(response_summary), 1, "expected a single ResponseSummary")
        response_summary = response_summary[0]
        next_page_url = [a for a in g.objects(response_summary, SPAPI['nextPageURL'])]
        self.assertEqual(len(next_page_url), 0, "did not expect nextPageURL")
        results_returned = [a for a in g.objects(response_summary, SPAPI['resultsReturned'])][0]
        self.assertEqual(results_returned, 1, "expected resultsReturned to be 1")
        total_result_count = [a for a in g.objects(response_summary, SPAPI['totalResultCount'])][0]
        self.assertEqual(total_result_count, 1, "expected totalResultCount to be 1")
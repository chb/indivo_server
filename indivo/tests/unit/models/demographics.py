import os
import settings
import json

from lxml import etree

from indivo.tests.internal_tests import InternalTests
from indivo.models import Demographics
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.document import TEST_DEMOGRAPHICS_DOCS
from indivo.tests.data.demographics import TEST_DEMOGRAPHICS_SDMX, TEST_DEMOGRAPHICS_SDMJ, TEST_DEMOGRAPHICS_RDFXML
from indivo.fields import CodedValueField
from django.db import models

URI_PREFIX = "http://indivo.org/"

class DemographicsModelUnitTests(InternalTests):
    def setUp(self):
        super(DemographicsModelUnitTests, self).setUp()

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0)
        
        # A demographics document
        self.document = self.createDocument(TEST_DEMOGRAPHICS_DOCS, 0, record=self.record)
        
        # demographics
        self.demographics = Demographics.from_xml(self.document.content)
        self.demographics.document = self.document
        self.demographics.save()
        self.record.demographics = self.demographics
        self.record.save()
        
    def tearDown(self):
        super(DemographicsModelUnitTests, self).tearDown()
        
    def test_from_xml(self):
        bad_xml = """<stuff>definitely not demographics</stuff>"""

        self.assertNotRaises(Exception, Demographics.from_xml, self.document.content)            
        self.assertRaises(ValueError, Demographics.from_xml, bad_xml)

    def test_as_json(self):
        expected_json = json.loads(TEST_DEMOGRAPHICS_SDMJ)
        generated_json = json.loads(self.demographics.as_json())
        
        del generated_json[0]['__documentid__']
        self.assertEqual(expected_json, generated_json)
        
    def test_as_xml(self):
        root = etree.XML(self.demographics.as_xml())
        
        demographics = root.findall('./Model')
        self.assertEqual(len(demographics), 1)
        demographics = demographics[0]
        
        # check Demographics
        self.assertEqual(len(demographics.findall('Field')), 22, "expected 22 fields on test Demographics")
        self.assertEqual(demographics.get('name'), 'Demographics')
        self.assertEqual(demographics.find('Field[@name="bday"]').text, '1939-11-15T00:00:00Z')
        self.assertEqual(demographics.find('Field[@name="email"]').text, 'test@fake.org')
        self.assertEqual(demographics.find('Field[@name="name_given"]').text, 'Bruce')
        self.assertEqual(demographics.find('Field[@name="name_family"]').text, 'Wayne')
        self.assertEqual(demographics.find('Field[@name="name_middle"]').text, 'Quentin')
        self.assertEqual(demographics.find('Field[@name="name_prefix"]').text, 'Mr')
        self.assertEqual(demographics.find('Field[@name="name_suffix"]').text, 'Jr')
        self.assertEqual(demographics.find('Field[@name="ethnicity"]').text, 'Scottish')
        self.assertEqual(demographics.find('Field[@name="race"]').text, 'caucasian')
        self.assertEqual(demographics.find('Field[@name="tel_1_type"]').text, 'h')
        self.assertEqual(demographics.find('Field[@name="tel_1_number"]').text, '555-5555')
        self.assertEqual(demographics.find('Field[@name="tel_1_preferred_p"]').text, 'true')
        self.assertEqual(demographics.find('Field[@name="tel_2_type"]').text, 'c')
        self.assertEqual(demographics.find('Field[@name="tel_2_number"]').text, '555-6666')
        self.assertEqual(demographics.find('Field[@name="tel_2_preferred_p"]').text, 'false')
        self.assertEqual(demographics.find('Field[@name="adr_region"]').text, 'secret')
        self.assertEqual(demographics.find('Field[@name="adr_country"]').text, 'USA')
        self.assertEqual(demographics.find('Field[@name="adr_postalcode"]').text, '90210')
        self.assertEqual(demographics.find('Field[@name="adr_city"]').text, 'Gotham')
        self.assertEqual(demographics.find('Field[@name="adr_street"]').text, '1007 Mountain Drive')

    def test_as_rdf(self):
        pass

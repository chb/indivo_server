from indivo.tests import data

doc_type = 'HBA1C'
label = 'testing_label'
external_doc_id = 'external_doc_test'
app_email = 'stephanie@apps.indivo.org'
app_secret = 'norepinephrine'
app2_email = 'problems@apps.indivo.org'
machine_app_email = 'stemapnea@apps.indivo.org'
machine_app_secret = 'neuronagility'

chrome_app_email= 'chrome@apps.indivo.org'
chrome_consumer_key = 'chrome'
chrome_consumer_secret ='chrome'

account = {'account_id' : 'stevezabak@informedcohort.org', 'username' : 'stevezabak', 'user_pass' : 'abc'}
account02 = {'account_id' : 'benadida@informedcohort.org', 'username' : 'benadida', 'user_pass' : 'test'}
account03 = {'account_id' : 'stevezabak2@informedcohort.org', 'username' : 'stevezabak2', 'user_pass' : 'abcd'}
alice_account = {'user_email' : 'alice@childrens.harvard.edu', 'user_pass' : 'abc'}
bob_account = {'user_email' : 'bob@childrens.harvard.edu', 'user_pass' : 'def'}
message01 = {'subject' : 'test 1', 'body' : 'hello world', 'message_id' : 'msg_01', 'severity': 'medium'}
message02 = {'subject' : 'test 2', 'body' : 'hello mars', 'message_id' : 'msg_02', 'severity': 'high'}

hba1c = [ {'value' : '3.4', 'datetime' : '2009-01-02T12:03:10Z'},
          {'value' : '9.2', 'datetime' : '2008-01-22T17:29:59Z'},
          {'value' : '4.8', 'datetime' : '2007-11-02T12:16:38Z'},
          {'value' : '4.6', 'datetime' : '2009-04-16T03:22:24Z'},
          {'value' : '3.1', 'datetime' : '2009-09-12T12:13:43Z'},
          {'value' : '3.3', 'datetime' : '2009-01-03T11:03:23Z'},
          {'value' : '1.9', 'datetime' : '2009-08-11T02:38:32Z'},
          {'value' : '1.3', 'datetime' : '2009-01-09T12:12:20Z'},
          {'value' : '6.7', 'datetime' : '2009-03-12T02:43:39Z'},
          {'value' : '3.7', 'datetime' : '2009-02-13T02:11:17Z'}]

doc00 = "<Document id='HELLOWORLD00' xmlns='http://indivo.org/vocab#'></Document>"
doc01 = "<Document id='HELLOWORLD01' xmlns='http://indivo.org/vocab#'></Document>"
doc02 = "<Document id='HELLOWORLD02' xmlns='http://indivo.org/vocab#'></Document>"
doc03 = "<Document id='HELLOWORLD03' xmlns='http://indivo.org/vocab#'></Document>"
doc04 = "<Document id='HELLOWORLD04' xmlns='http://indivo.org/vocab#'></Document>"
doc05 = "<Document id='HELLOWORLD05' xmlns='http://indivo.org/vocab#'></Document>"
doc06 = "<Document id='HELLOWORLD06' xmlns='http://indivo.org/vocab#'></Document>"
doc07 = "<Document id='HELLOWORLD07' xmlns='http://indivo.org/vocab#'></Document>"
doc08 = "<Document id='HELLOWORLD08' xmlns='http://indivo.org/vocab#'></Document>"
doc09 = "<Document id='HELLOWORLD09' xmlns='http://indivo.org/vocab#'></Document>"
doc10 = "<Document id='HELLOWORLD10' xmlns='http://indivo.org/vocab#'></Document>"
doc11 = "<Document id='HELLOWORLD11' xmlns='http://indivo.org/vocab#'></Document>"
doc12 = "<Document id='HELLOWORLD12' xmlns='http://indivo.org/vocab#'></Document>"
doc13 = "<Document id='HELLOWORLD13' xmlns='http://indivo.org/vocab#'></Document>"
doc14 = "<Document id='HELLOWORLD14' xmlns='http://indivo.org/vocab#'></Document>"
doc15 = "<Document id='HELLOWORLD15' xmlns='http://indivo.org/vocab#'></Document>"
doc16 = "<Document id='HELLOWORLD16' xmlns='http://indivo.org/vocab#'></Document>"
doc17 = "<Document id='HELLOWORLD17' xmlns='http://indivo.org/vocab#'></Document>"
doc18 = "<Document id='HELLOWORLD18' xmlns='http://indivo.org/vocab#'></Document>"
doc19 = "<Document id='HELLOWORLD19' xmlns='http://indivo.org/vocab#'></Document>"
doc20 = "<Document id='HELLOWORLD20' xmlns='http://indivo.org/vocab#'></Document>"

demographics = '''<?xml version="1.0" encoding="utf-8" ?>
                    <Demographics xmlns="http://indivo.org/vocab/xml/documents#">
                        <dateOfBirth>1939-11-15</dateOfBirth>
                        <gender>male</gender>
                        <email>test@fake.org</email>
                        <ethnicity>Scottish</ethnicity>
                        <preferredLanguage>english</preferredLanguage>
                        <race>caucasian</race>
                        <Name>
                            <familyName>Wayne</familyName>
                            <givenName>Bruce</givenName>
                            <prefix>Mr</prefix>
                            <suffix>Jr</suffix>
                        </Name>
                        <Telephone>
                            <type>h</type>
                            <number>555-5555</number>
                            <preferred>true</preferred>
                        </Telephone>
                        <Telephone>
                            <type>c</type>
                            <number>555-6666</number>
                        </Telephone>
                        <Address>
                            <country>USA</country>
                            <city>Gotham</city>
                            <postalCode>90210</postalCode>
                            <region>secret</region>
                            <street>1007 Mountain Drive</street>
                        </Address>
                    </Demographics>'''
                    
demographics2 = '''<?xml version="1.0" encoding="utf-8" ?>
                    <Demographics xmlns="http://indivo.org/vocab/xml/documents#">
                        <dateOfBirth>1939-11-15</dateOfBirth>
                        <gender>male</gender>
                        <email>test@fake.org</email>
                        <ethnicity>Scottish</ethnicity>
                        <preferredLanguage>english</preferredLanguage>
                        <race>caucasian</race>
                        <Name>
                            <familyName>McTest</familyName>
                            <givenName>Steve</givenName>
                            <prefix>Mr</prefix>
                            <suffix>Jr</suffix>
                        </Name>
                        <Telephone>
                            <type>home</type>
                            <number>555-5555</number>
                            <preferred>true</preferred>
                        </Telephone>
                        <Telephone>
                            <type>cell</type>
                            <number>555-6666</number>
                        </Telephone>
                        <Address>
                            <country>USA</country>
                            <city>Gotham</city>
                            <postalCode>90210</postalCode>
                            <region>secret</region>
                            <street>1007 Mountain Drive</street>
                        </Address>
                    </Demographics>'''
                    
# an allergy with the wrong allergy schema, should fail too
malformed_allergy = data.reports.allergy._TEST_ALLERGIES_INVALID[0]

allergy = data.reports.allergy._TEST_ALLERGIES[0]

immunization = data.reports.immunization._TEST_IMMUNIZATIONS[0]

measurement00 = "<HBA1C xmlns='http://indivo.org/vocab/xml/documents#' value='1.77' unit='percent' datetime='2009-07-22T01:00:00.000Z' />"
measurement01 = "<HBA1C xmlns='http://indivo.org/vocab/xml/documents#' value='2.13' unit='percent' datetime='2009-06-17T03:00:00.034Z' />"
measurement02 = "<HBA1C xmlns='http://indivo.org/vocab/xml/documents#' value='3.13' unit='percent' datetime='2009-06-17T03:00:00Z' />"

medication = """<Medication xmlns="http://indivo.org/vocab/xml/documents#"> <dateStarted>2009-02-05</dateStarted> <name type="http://indivo.org/codes/meds#" abbrev="c2i" value="COX2 Inhibitor">COX2 Inhibitor</name>   <brandName type="http://indivo.org/codes/meds#" abbrev="vioxx" value="Vioxx">Vioxx</brandName> <dose> <value>3</value> <unit type="http://indivo.org/codes/units#" value="pills" abbrev="p">pills</unit> </dose> <route type="http://indivo.org/codes/routes#" value="PO">By Mouth</route> <strength> <value>100</value> <unit type="http://indivo.org/codes/units#" value="mg" abbrev="mg">mg</unit> </strength> <frequency type="http://indivo.org/codes/frequency#" value="daily" abbrev="daily">every 12 hours</frequency> <prescription> <by> <name>Dr. Ken Mandl</name> <institution>Children's Hospital Boston</institution> </by> <on>2009-02-01</on> <stopOn>2010-01-31</stopOn> <dispenseAsWritten>true</dispenseAsWritten> <duration>P2M</duration> <refillInfo>once a month for 3 months</refillInfo> <instructions>don't take them all at once!</instructions> </prescription> </Medication>"""

medication_no_codes = """<Medication xmlns="http://indivo.org/vocab/xml/documents#"> <dateStarted>2009-02-05</dateStarted> <name>COX2 Inhibitor</name>   <brandName>Vioxx</brandName> <dose> <textValue>3 pills</textValue></dose> <route>By Mouth</route> <strength> <value>100</value> <unit>mg</unit> </strength> <frequency>every 12 hours</frequency> <prescription> <by> <name>Dr. Ken Mandl</name> <institution>Children's Hospital Boston</institution> </by> <on>2009-02-01</on> <stopOn>2010-01-31</stopOn> <dispenseAsWritten>true</dispenseAsWritten> <duration>P2M</duration> <refillInfo>once a month for 3 months</refillInfo> <instructions>don't take them all at once!</instructions> </prescription> </Medication>"""

medication2 = "<Medication xmlns='http://indivo.org/vocab/xml/documents#'> <name type='http://indivo.org/codes/meds#' value='Tylenol' abbrev='Tylenol'>Tylenol</name><dose><textValue>2</textValue></dose> <frequency type='http://indivo.org/codes/frequency#' value='225756002' abbrev='q4'>every 4 hours</frequency> </Medication>"

problem = "<Problem xmlns='http://indivo.org/vocab/xml/documents#'> <dateOnset>2009-05-16T12:00:00Z</dateOnset> <dateResolution>2009-05-16T16:00:00Z</dateResolution> <name type='http://codes.indivo.org/problems/' value='123' abbrev='MI'>Myocardial Infarction</name> <comments>mild heart attack</comments> <diagnosedBy>Steve Zabak</diagnosedBy> </Problem>"

problem_no_code = "<Problem xmlns='http://indivo.org/vocab/xml/documents#'> <dateOnset>2009-05-16T12:00:00Z</dateOnset> <dateResolution>2009-05-16T16:00:00Z</dateResolution> <name>Myocardial Infarction</name> <comments>mild heart attack</comments> <diagnosedBy>Steve Zabak</diagnosedBy> </Problem>"

problem_no_dates = "<Problem xmlns='http://indivo.org/vocab/xml/documents#'> <name>Myocardial Infarction</name> <comments>mild heart attack</comments> <diagnosedBy>Steve Zabak</diagnosedBy> </Problem>"

procedure = "<Procedure xmlns='http://indivo.org/vocab/xml/documents#'> <datePerformed>2009-05-16T12:00:00Z</datePerformed> <name type='http://codes.indivo.org/procedures#' value='85' abbrev='append'>Appendectomy</name> <provider> <name>Kenneth Mandl</name> <institution>Children's Hospital Boston</institution> </provider> </Procedure>"

procedure_no_code = "<Procedure xmlns='http://indivo.org/vocab/xml/documents#'> <datePerformed>2009-05-16T12:00:00Z</datePerformed> <name>Appendectomy</name> <provider> <name>Kenneth Mandl</name> <institution>Children's Hospital Boston</institution> </provider> </Procedure>"

equipment = "<Equipment xmlns='http://indivo.org/vocab/xml/documents#'><dateStarted>2010-09-01</dateStarted><name>Tractor</name> <vendor>John Deer</vendor> <description>Hello World</description></Equipment>"

equipment02 = '<Equipment xmlns="http://indivo.org/vocab/xml/documents#"><dateStarted>2010-09-02</dateStarted><name>cane</name></Equipment>'

vital_sign = data.reports.vital._TEST_VITALS[0]

patient_access_key = "<PatientAccessKey> <record_id>456</record_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> <access_key> <patient_id>123</patient_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> </access_key> </PatientAccessKey>"
access_key = "<AccessKey> <record_id>456</record_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> <access_key> <patient_id>123</patient_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> </access_key> </AccessKey>"

lab = data.reports.lab._TEST_LABS[0]

clinical_note= """
<SimpleClinicalNote xmlns="http://indivo.org/vocab/xml/documents#">
  <dateOfVisit>2010-02-02T12:00:00Z</dateOfVisit>
  <finalizedAt>2010-02-03T13:54:03Z</finalizedAt>
  <visitType type="http://codes.indivo.org/visit-types#" value="acute">Acute Care</visitType>
  <visitLocation>Longfellow Medical</visitLocation>
  <specialty type="http://codes.indivo.org/specialties#" value="hem-onc">Hematology/Oncology</specialty>

  <signature>
    <at>2010-02-03T13:12:00Z</at>
    
    <provider>
      <name>Kenneth Mandl</name>
      <institution>Children's Hospital Boston</institution>
    </provider>
  </signature>

  <signature>
    <at>2010-02-03T13:14:00Z</at>
    
    <provider>
      <name>Isaac Kohane</name>
      <institution>Children's Hospital Boston</institution>
    </provider>
  </signature>

  <chiefComplaint>stomach ache</chiefComplaint>
  <content>
    (repeated to test length)
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
    Patient presents with a serious condition of X and is probably going to need to see a doctor about Y and Z.
  </content>
</SimpleClinicalNote>
"""

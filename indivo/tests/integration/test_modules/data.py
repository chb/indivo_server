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

demographics = '''<Demographics xmlns="http://indivo.org/vocab/xml/documents#"> <foo>bar</foo></Demographics>'''
contact = '''<Contact id="5326" xmlns="http://indivo.org/vocab/xml/documents#"> <name> <fullName>Sebastian Rockwell Cotour</fullName> <givenName>Sebastian</givenName> <familyName>Cotour</familyName> </name> <email type="personal"> <emailAddress>scotour@hotmail.com</emailAddress> </email> <email type="work"> <emailAddress>sebastian.cotour@childrens.harvard.edu</emailAddress> </email> <address type="home"> <streetAddress>15 Waterhill Ct.</streetAddress> <postalCode>53326</postalCode> <locality>New Brinswick</locality> <region>Montana</region> <country>US</country> <timeZone>-7GMT</timeZone> </address> <location type="home"> <latitude>47N</latitude> <longitude>110W</longitude> </location> <phoneNumber type="home">5212532532</phoneNumber> <phoneNumber type="work">6217233734</phoneNumber> <instantMessengerName protocol="aim">scotour</instantMessengerName> </Contact>'''

contact02 = '''<Contact id="5326" xmlns="http://indivo.org/vocab/xml/documents#"> <name> <fullName>Sebastian Rockwell Cotour the Second</fullName> <givenName>Sebastian</givenName> <familyName>Cotour</familyName> </name> <email type="personal"> <emailAddress>scotour@hotmail.com</emailAddress> </email> <email type="work"> <emailAddress>sebastian.cotour@childrens.harvard.edu</emailAddress> </email> <address type="home"> <streetAddress>15 Waterhill Ct.</streetAddress> <postalCode>53326</postalCode> <locality>New Brinswick</locality> <region>Montana</region> <country>US</country> <timeZone>-7GMT</timeZone> </address> <location type="home"> <latitude>47N</latitude> <longitude>110W</longitude> </location> <phoneNumber type="home">5212532532</phoneNumber> <phoneNumber type="work">6217233734</phoneNumber> <instantMessengerName protocol="aim">scotour</instantMessengerName> </Contact>'''

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

vital_sign2 = "<VitalSign xmlns='http://indivo.org/vocab/xml/documents#'> <dateMeasured>2009-05-16T15:23:21Z</dateMeasured> <name type='http://codes.indivo.org/vitalsigns/' value='123' abbrev='BPsys'>Blood Pressure Systolic</name> <value>145</value> <unit type='http://codes.indivo.org/units/' value='31' abbrev='mmHg'>millimeters of mercury</unit> <site>left arm</site> <position>sitting down</position> </VitalSign>"
vital_sign = "<VitalSign xmlns='http://indivo.org/vocab/xml/documents#'> <dateMeasured>2009-05-16T15:23:21Z</dateMeasured> <name type='http://codes.indivo.org/vitalsigns/' value='123' abbrev='weight'>weight test</name> <value>185</value> <unit type='http://codes.indivo.org/units/' value='31' abbrev='lbs'>pounds</unit> <site /> <position /> </VitalSign>"
patient_access_key = "<PatientAccessKey> <record_id>456</record_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> <access_key> <patient_id>123</patient_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> </access_key> </PatientAccessKey>"
access_key = "<AccessKey> <record_id>456</record_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> <access_key> <patient_id>123</patient_id> <token>z8j38em</token> <token_secret>hs92jwl</token_secret> </access_key> </AccessKey>"
lab01 = """<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> <dateMeasured>2009-07-16T12:00:00Z</dateMeasured> <labType>hematology</labType> <laboratory> <name>Quest</name> <address>300 Longwood Ave, Boston MA 02215</address> </laboratory> <labPanel> <name type="http://codes.indivo.org/labs/panels#" abbrev="cbc" value="CBC">CBC</name> <labTest xsi:type="SingleResultLabTest"> <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> <name type="http://codes.indivo.org/labs/tests#" abbrev="Hct" value="evf">evf</name> <final>true</final> <result xsi:type="ResultInRange"> <flag type="http://codes.indivo.org/hl7/abnormal-flags#" abbrev="A" value="abnormal" /> <valueAndUnit> <value>49</value> <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> </valueAndUnit> <normalRange> <minimum>44</minimum> <maximum>48</maximum> <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> </normalRange> <nonCriticalRange> <minimum>42</minimum> <maximum>50</maximum> <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> </nonCriticalRange> </result> </labTest> <labTest xsi:type="SingleResultLabTest"> <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> <name type="http://codes.indivo.org/labs/tests#" abbrev="hiv" value="HIV">HIV</name> <final>true</final> <result xsi:type="ResultInSet"> <value>negative</value> <option normal="false">positive</option> <option normal="true">negative</option> <option normal="true" description="insufficient sample">inconclusive</option> </result> </labTest> </labPanel> <comments>was looking pretty sick</comments> </Lab>"""
lab02 = """<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> <dateMeasured>2009-07-16T12:00:00Z</dateMeasured> <labType>microbiology</labType> <laboratory> <name>Quest</name> <address>300 Longwood Ave, Boston MA 02215</address> </laboratory> <labTest xsi:type="MicroWithCultureLabTest"> <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> <name type="http://codes.indivo.org/labs/tests#" abbrev="mic" value="MIC">MIC</name> <final>true</final><source></source><observation isolate="whoknows"> <time>2009-07-16T12:56:00Z</time></observation> <observation isolate="whoknows"> <time>2009-07-16T13:45:00Z</time> <microbialDensity><value> <value>100000</value> <unit type="http://codes.indivo.org/units#" abbrev="cfu" value="CFU" /></value> </microbialDensity><cultureCondition>aerobic</cultureCondition> <gram>true</gram> <organization>clusters</organization></observation> <result isolate="what?" identity="1"> <organism>E. Coli</organism> <interpretation>stop eating bad beef</interpretation> </result> <result isolate="who?" identity="2"> <organism>Crazy Bugs</organism> <interpretation>stop eating things that look like beef but aren't</interpretation> </result> </labTest> </Lab>"""
lab03= """<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <dateMeasured>2010-09-01T00:00:00Z</dateMeasured>
   <labType>1,25-Dihydroxy Vitamin D</labType>
   <labTest xsi:type="SingleResultLabTest">
      <dateMeasured>2010-09-03T00:00:00Z</dateMeasured>
      <name abbrev="1,25-Dihydroxy Vitamin D">1,25-Dihydroxy Vitamin D</name>
      <final>false</final>
      <result xsi:type="ResultInRange">
         <flag type="http://indivo.org/codes/hl7-abnormal-flags#" value="H" abbrev="H">High</flag>
         <valueAndUnit>
            <value>119.0</value>
            <unit type="http://indivo.org/codes/units#" value="pg/mL" abbrev="pg/mL">pg/mL</unit>
         </valueAndUnit>
      </result>
   </labTest>
   <comments>TEST INFORMATION: Vitamin D, 1,25-Dihydroxy   This test is primarily indicated during patient evaluation for hypercalcemia and renal failure. A normal result does not rule out Vitamin D deficiency. The recommended test for diagnosing Vitamin D deficiency is Vitamin D 25-hydroxy (0080379). Test performed at ARUP Laboratories, 500 Chipeta Way, Salt Lake City, Utah, 84108.</comments>
</Lab>"""

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

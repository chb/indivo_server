from base import report_content_to_test_docs

_TEST_MEDICATIONS = [
    """
<Medication xmlns="http://indivo.org/vocab/xml/documents#">
  <dateStarted>2009-02-05</dateStarted> 
  <name type="http://indivo.org/codes/meds#" abbrev="c2i" value="COX2 Inhibitor">COX2 Inhibitor</name>
  <brandName type="http://indivo.org/codes/meds#" abbrev="vioxx" value="Vioxx">Vioxx</brandName>
  <dose>
    <value>3</value>
    <unit type="http://indivo.org/codes/units#" value="pills" abbrev="p">pills</unit>
  </dose>
  <route type="http://indivo.org/codes/routes#" value="PO">By Mouth</route>
  <strength>
    <value>100</value>
    <unit type="http://indivo.org/codes/units#" value="mg" abbrev="mg">mg</unit>
  </strength>
  <frequency type="http://indivo.org/codes/frequency#" value="daily" abbrev="daily">every 12 hours</frequency>
  <prescription>
    <by>
      <name>Dr. Ken Mandl</name>
      <institution>Children's Hospital Boston</institution>
    </by>
    <on>2009-02-01</on> 
    <stopOn>2010-01-31</stopOn>
    <dispenseAsWritten>true</dispenseAsWritten>
    <duration>P2M</duration>
    <refillInfo>once a month for 3 months</refillInfo>
    <instructions>don't take them all at once!</instructions>
  </prescription>
</Medication>
""",

    """
<Medication xmlns="http://indivo.org/vocab/xml/documents#">
  <dateStarted>2009-03-05</dateStarted>
  <name>COX2 Inhibitor</name>
  <brandName>Vioxx</brandName>
  <dose>
    <textValue>3 pills</textValue>
  </dose>
  <route>By Mouth</route>
  <strength>
    <value>100</value>
    <unit>mg</unit>
  </strength>
  <frequency>every 12 hours</frequency> 
  <prescription>
    <by>
      <name>Dr. Ken Mandl</name>
      <institution>Children's Hospital Boston</institution>
    </by>
    <on>2009-02-01</on>
    <stopOn>2010-01-31</stopOn>
    <dispenseAsWritten>true</dispenseAsWritten>
    <duration>P2M</duration>
    <refillInfo>once a month for 3 months</refillInfo>
    <instructions>don't take them all at once!</instructions>
  </prescription>
</Medication>
""",

    """
<Medication xmlns='http://indivo.org/vocab/xml/documents#'>
  <dateStarted>2009-02-05</dateStarted>
  <name type='http://indivo.org/codes/meds#' value='Tylenol' abbrev='Tylenol'>Tylenol</name>
  <dose>
    <textValue>2</textValue>
  </dose>
  <frequency type='http://indivo.org/codes/frequency#' value='225756002' abbrev='q4'>every 4 hours</frequency>
</Medication>
""",

]

TEST_MEDICATIONS = report_content_to_test_docs(_TEST_MEDICATIONS)

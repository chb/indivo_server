from base import report_content_to_test_docs

_TEST_VITALS = [
    """
<VitalSign xmlns='http://indivo.org/vocab/xml/documents#'>
  <dateMeasured>2009-05-16T15:23:21Z</dateMeasured>
  <name type='http://codes.indivo.org/vitalsigns/' value='123' abbrev='BPsys'>Blood Pressure Systolic</name>
  <value>145</value>
  <unit type='http://codes.indivo.org/units/' value='31' abbrev='mmHg'>millimeters of mercury</unit>
  <site>left arm</site>
  <position>sitting down</position>
</VitalSign>
""",

    """
<VitalSign xmlns='http://indivo.org/vocab/xml/documents#'>
  <dateMeasured>2009-05-16T15:23:21Z</dateMeasured>
  <name type='http://codes.indivo.org/vitalsigns/' value='123' abbrev='weight'>weight test</name>
  <value>185</value>
  <unit type='http://codes.indivo.org/units/' value='31' abbrev='lbs'>pounds</unit>
  <site />
  <position />
</VitalSign>
""",
]

TEST_VITALS = report_content_to_test_docs(_TEST_VITALS)

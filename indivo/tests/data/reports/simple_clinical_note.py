from base import report_content_to_test_docs

_TEST_CLINICAL_NOTES = [
    """
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
""",
]

TEST_CLINICAL_NOTES = report_content_to_test_docs(_TEST_CLINICAL_NOTES)

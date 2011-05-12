from indivo.tests.data.base import TestXMLDoc

_TEST_ALLERGIES_INVALID = [
    # an allergy with a bad date that should trigger a validation problem
    """
<Allergy xmlns='http://indivo.org/vocab/xml/documents#'> 
  <dateDiagnosed>2009-05-</dateDiagnosed> 
  <diagnosedBy>Children's Hospital Boston</diagnosedBy> 
  <allergen> 
    <type type='http://codes.indivo.org/codes/allergentypes/' value='drugs'>Drugs</type> 
    <name type='http://codes.indivo.org/codes/allergens/' value='penicillin'>Penicillin</name> 
  </allergen> 
  <reaction>blue rash</reaction> 
  <specifics>this only happens on weekends</specifics> 
</Allergy>
""",

    # an allergy with the wrong allergy schema, should fail too
    """
<Allergy xmlns='http://indivo.org/vocab/xml/documents#'> 
  <dateDiagnosed>2009-05-12</dateDiagnosed> 
  <allergen> 
    <name>foo</name> 
    <type type='http://codes.indivo.org/codes/allergentypes/' value='drugs'>Drugs</type> 
    <name type='http://codes.indivo.org/codes/allergens/' value='penicillin'>Penicillin</name> 
  </allergen> 
  <reaction>blue rash</reaction> 
  <specifics>this only happens on weekends</specifics> 
</Allergy>
""",
]

_TEST_ALLERGIES = [
    """
<Allergy xmlns='http://indivo.org/vocab/xml/documents#'> 
  <dateDiagnosed>2009-05-16</dateDiagnosed> 
  <diagnosedBy>Children's Hospital Boston</diagnosedBy> 
  <allergen> 
    <type type='http://codes.indivo.org/codes/allergentypes/' value='drugs'>Drugs</type> 
    <name type='http://codes.indivo.org/codes/allergens/' value='penicillin'>Penicillin</name> 
  </allergen> 
  <reaction>blue rash</reaction> 
  <specifics>this only happens on weekends</specifics> 
</Allergy>
""",

    """
<Allergy xmlns='http://indivo.org/vocab/xml/documents#'> 
  <dateDiagnosed>2009-05-16</dateDiagnosed> 
  <diagnosedBy>Children's Hospital Boston</diagnosedBy> 
  <allergen> 
    <type type='http://codes.indivo.org/codes/allergentypes/' value='drugs'>Drugs</type> 
    <name type='http://codes.indivo.org/codes/allergens/' value='penicillin'>Penicillin</name> 
  </allergen> 
  <reaction>red rash</reaction> 
  <specifics>hello</specifics> 
</Allergy>
""",

    """
<Allergy xmlns='http://indivo.org/vocab/xml/documents#'> 
  <dateDiagnosed>2009-05-16</dateDiagnosed> 
  <diagnosedBy>Children's Hospital Boston</diagnosedBy> 
  <allergen> 
    <type type='http://codes.indivo.org/codes/allergentypes/' value='drugs'>Drugs</type> 
    <name type='http://codes.indivo.org/codes/allergens/' value='penicillin'>Penicillin</name> 
  </allergen> 
  <reaction>green rash</reaction> 
  <specifics>world</specifics> 
</Allergy>
""",


    """
<Allergy xmlns='http://indivo.org/vocab/xml/documents#'> 
  <dateDiagnosed>2009-05-16</dateDiagnosed> 
  <diagnosedBy>Children's Hospital Boston</diagnosedBy> 
  <allergen> 
    <type>Drugs</type> 
    <name>Penicillin</name> 
  </allergen> 
  <reaction>green rash</reaction> 
  <specifics>world</specifics> 
</Allergy>
""",

]

TEST_ALLERGIES_INVALID = [TestXMLDoc(raw_data) for raw_data in _TEST_ALLERGIES_INVALID]
TEST_ALLERGIES = [TestXMLDoc(raw_data) for raw_data in _TEST_ALLERGIES]

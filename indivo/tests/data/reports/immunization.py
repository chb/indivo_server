from base import report_content_to_test_docs

_TEST_IMMUNIZATIONS = [
    """
<Immunization xmlns='http://indivo.org/vocab/xml/documents#'>
  <dateAdministered>2009-05-16T00:00:00Z</dateAdministered>
  <administeredBy>Children's Hospital Boston</administeredBy>
  <vaccine>
    <type type='http://codes.indivo.org/codes/vaccinetypes/' value='hep-B' abbrev='hepb'>Hepatitis B</type>
    <manufacturer>Oolong Pharmaceuticals</manufacturer>
    <lot>AZ1234567</lot>
    <expiration>2009-06-01</expiration>
  </vaccine>
  <sequence>2</sequence>
  <anatomicSurface type='http://codes.indivo.org/codes/anatomicsurfaces/' value='shoulder' abbrev='shoulder'>Shoulder</anatomicSurface>
  <adverseEvent>pain and rash</adverseEvent>
</Immunization>
""",

"""
<Immunization xmlns='http://indivo.org/vocab/xml/documents#'> 
  <dateAdministered>2008-05-12T00:00:00Z</dateAdministered>
  <vaccine>
    <type type='http://codes.indivo.org/codes/vaccinetypes/' value='82' abbrev='adenovirus, NOS'>adenovirus vaccine, NOS</type>
  </vaccine>
  <sequence>2</sequence>
</Immunization>
""",
]

TEST_IMMUNIZATIONS = report_content_to_test_docs(_TEST_IMMUNIZATIONS)

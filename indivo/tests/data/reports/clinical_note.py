from base import report_content_to_test_docs

_TEST_CLINICAL_NOTES = [
    """
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="ClinicalNote">
    <Field name="date">2012-05-17</Field>
    <Field name="title">Telephone note</Field>
    <Field name="format">http://purl.org/NET/mediatypes/text/plain</Field>
    <Field name="value">Patient's mother telephoned to say that he no longer needs documentation of a sports physical for school</Field>
    <Field name="provider_name_given">Josuha</Field>
    <Field name="provider_name_family">Mandel</Field>
  </Model>
</Models>
""",
]

TEST_CLINICAL_NOTES = report_content_to_test_docs(_TEST_CLINICAL_NOTES)

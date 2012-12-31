from base import report_content_to_test_docs

_TEST_IMMUNIZATIONS = [
    """
<Models xmlns='http://indivo.org/vocab/xml/documents#'>
  <Model name="Immunization">
    <Field name="date">2009-05-16T12:00:00Z</Field>
    <Field name="administration_status_title">Not Administered</Field>
    <Field name="administration_status_code_title">Not Administered</Field>
    <Field name="administration_status_code_system">http://smartplatforms.org/terms/codes/ImmunizationAdministrationStatus#</Field>
    <Field name="administration_status_code_identifier">notAdministered</Field> 
    <Field name="product_class_title">TYPHOID</Field>
    <Field name="product_class_code_title">TYPHOID</Field>
    <Field name="product_class_code_system">http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=vg#</Field>
    <Field name="product_class_code_identifier">TYPHOID</Field>
    <Field name="product_name_title">typhoid, oral</Field>
    <Field name="product_name_code_title">typhoid, oral</Field>
    <Field name="product_name_code_system">http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=cvx#</Field>
    <Field name="product_name_code_identifier">25</Field>
    <Field name="refusal_reason_title">Allergy to vaccine/vaccine components, or allergy to eggs</Field>
    <Field name="refusal_reason_code_title">Allergy to vaccine/vaccine components, or allergy to eggs</Field>
    <Field name="refusal_reason_code_system">http://smartplatforms.org/terms/codes/ImmunizationRefusalReason#</Field>
    <Field name="refusal_reason_code_identifier">allergy</Field>
  </Model>
</Models>
""",
]

TEST_IMMUNIZATIONS = report_content_to_test_docs(_TEST_IMMUNIZATIONS)

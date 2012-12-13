from base import report_content_to_test_docs

_TEST_PROBLEMS = [
    """
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Problem">
    <Field name="startDate">2009-05-16T12:00:00Z</Field>
    <Field name="endDate">2011-08-22T00:00:00Z</Field>
    <Field name="name_title">Backache 1</Field>
    <Field name="name_code_title">Backache (Finding)</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">161891005</Field>
    <Field name="encounters">
      <Models>
          <Model name="Encounter">
            <Field name="startDate">2010-02-16T12:00:00Z</Field>
            <Field name="endDate">2010-02-16T16:00:00Z</Field>
            <Field name="facility_name">Wonder Hospital</Field>
            <Field name="facility_adr_country">Australia</Field>
            <Field name="facility_adr_city">WonderCity</Field>
            <Field name="facility_adr_postalcode">5555</Field>
            <Field name="facility_adr_street">111 Lake Drive</Field> 
            <Field name="provider_dea_number">325555555</Field>
            <Field name="provider_npi_number">5235235</Field>
            <Field name="provider_email">joshua.mandel@fake.emailserver.com</Field>
            <Field name="provider_name_given">Josuha</Field>
            <Field name="provider_name_family">Mandel</Field>
            <Field name="provider_tel_1_type">w</Field>
            <Field name="provider_tel_1_number">1-235-947-3452</Field>
            <Field name="provider_tel_1_preferred_p">true</Field>
            <Field name="type_code_title">Ambulatory encounter</Field>
            <Field name="type_code_system">http://smartplatforms.org/terms/codes/EncounterType#</Field>
            <Field name="type_code_identifier">ambulatory</Field>
          </Model>
          <Model name="Encounter">
            <Field name="startDate">2009-05-16T12:00:00Z</Field>
            <Field name="endDate">2009-05-16T16:00:00Z</Field>
            <Field name="facility_name">Wonder Hospital</Field>
            <Field name="facility_adr_country">Australia</Field>
            <Field name="facility_adr_city">WonderCity</Field>
            <Field name="facility_adr_postalcode">5555</Field>
            <Field name="facility_adr_street">111 Lake Drive</Field> 
            <Field name="provider_dea_number">325555555</Field>
            <Field name="provider_npi_number">5235235</Field>
            <Field name="provider_email">joshua.mandel@fake.emailserver.com</Field>
            <Field name="provider_name_given">Josuha</Field>
            <Field name="provider_name_family">Mandel</Field>
            <Field name="provider_tel_1_type">w</Field>
            <Field name="provider_tel_1_number">1-235-947-3452</Field>
            <Field name="provider_tel_1_preferred_p">true</Field>
            <Field name="type_code_title">Ambulatory encounter</Field>
            <Field name="type_code_system">http://smartplatforms.org/terms/codes/EncounterType#</Field>
            <Field name="type_code_identifier">ambulatory</Field>
          </Model>
        </Models>
    </Field>
  </Model>
</Models>
""",
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Problem">
    <Field name="startDate">2009-05-16</Field>
    <Field name="name_title">Backache 2</Field>
    <Field name="name_code_title">Backache (Finding)</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">161891005</Field>
  </Model>
</Models>
""",
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Problem">
    <Field name="startDate">2009-06-16</Field>
    <Field name="name_title">Backache 3</Field>
    <Field name="name_code_title">Backache (Finding)</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">161891005</Field>
  </Model>
</Models>
""",
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Problem">
    <Field name="startDate">2010-02-22</Field>
    <Field name="name_title">Backache 4</Field>
    <Field name="name_code_title">Backache (Finding)</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">161891005</Field>
  </Model>
</Models>
""",
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Problem">
    <Field name="startDate">2010-05-16</Field>
    <Field name="name_title">Backache 5</Field>
    <Field name="name_code_title">Backache (Finding)</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">161891005</Field>
  </Model>
</Models>
""",
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Problem">
    <Field name="startDate">2010-05-17</Field>
    <Field name="name_title">Backache 6</Field>
    <Field name="name_code_title">Backache (Finding)</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">161891005</Field>
  </Model>
</Models>
""",
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Problem">
    <Field name="startDate">2011-03-04</Field>
    <Field name="name_title">Backache 7</Field>
    <Field name="name_code_title">Backache (Finding)</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">161891005</Field>
  </Model>
</Models>
""",
]

TEST_PROBLEMS = report_content_to_test_docs(_TEST_PROBLEMS)


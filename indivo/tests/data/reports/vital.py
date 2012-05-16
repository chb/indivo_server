from base import report_content_to_test_docs

_TEST_VITALS = [
    """
<Models>
  <Model name="VitalSigns">
    <Field name="date">2009-05-16T12:00:00Z</Field>
    <Field name="encounter">
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
        <Field name="encounterType_title">Ambulatory encounter</Field>
        <Field name="encounterType_system">http://smartplatforms.org/terms/codes/EncounterType#</Field>
        <Field name="encounterType_identifier">ambulatory</Field>
      </Model>
    </Field>
    <Field name="bp_position_title">Sitting</Field>
    <Field name="bp_position_identifier">33586001</Field>
    <Field name="bp_position_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="bp_site_title">Right arm</Field>
    <Field name="bp_site_identifier">368209003</Field>
    <Field name="bp_site_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="bp_method_title">Auscultation</Field>
    <Field name="bp_method_identifier">auscultation</Field>
    <Field name="bp_method_system">http://smartplatforms.org/terms/codes/BloodPressureMethod#</Field>
    <Field name="bp_diastolic_unit">mm[Hg]</Field>
    <Field name="bp_diastolic_value">82</Field>
    <Field name="bp_diastolic_name_title">Intravascular diastolic</Field>
    <Field name="bp_diastolic_name_identifier">8462-4</Field>
    <Field name="bp_diastolic_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="bp_systolic_unit">mm[Hg]</Field>
    <Field name="bp_systolic_value">132</Field>
    <Field name="bp_systolic_name_title">Intravascular systolic</Field>
    <Field name="bp_systolic_name_identifier">8480-6</Field>
    <Field name="bp_systolic_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="bmi_unit">kg/m2</Field>
    <Field name="bmi_value">21.8</Field>
    <Field name="bmi_name_title">Body mass index</Field>
    <Field name="bmi_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="bmi_name_identifier">39156-5</Field>
    <Field name="heart_rate_unit">{beats}/min</Field>
    <Field name="heart_rate_value">70</Field>
    <Field name="heart_rate_name_title">Heart rate</Field>
    <Field name="heart_rate_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="heart_rate_name_identifier">8867-4</Field>
    <Field name="height_unit">m</Field>
    <Field name="height_value">1.8</Field>
    <Field name="height_name_title">Body height</Field>
    <Field name="height_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="height_name_identifier">8302-2</Field>
    <Field name="oxygen_saturation_unit">%{HemoglobinSaturation}</Field>
    <Field name="oxygen_saturation_value">99</Field>
    <Field name="oxygen_saturation_name_title">Oxygen saturation</Field>
    <Field name="oxygen_saturation_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="oxygen_saturation_name_identifier">2710-2</Field>
    <Field name="respiratory_rate_unit">{breaths}/min</Field>
    <Field name="respiratory_rate_value">16</Field>
    <Field name="respiratory_rate_name_title">Respiration rate</Field>
    <Field name="respiratory_rate_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="respiratory_rate_name_identifier">9279-1</Field>
    <Field name="temperature_unit">Cel</Field>
    <Field name="temperature_value">37</Field>
    <Field name="temperature_name_title">Body temperature</Field>
    <Field name="temperature_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="temperature_name_identifier">8310-5</Field>
    <Field name="weight_unit">kg</Field>
    <Field name="weight_value">70.8</Field>
    <Field name="weight_name_title">Body weight</Field>
    <Field name="weight_name_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="weight_name_identifier">3141-9</Field>
  </Model>
</Models>
""",
]

TEST_VITALS = report_content_to_test_docs(_TEST_VITALS)

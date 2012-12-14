from base import report_content_to_test_docs

_TEST_LABS = [
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="LabResult">
    <Field name="date">2009-05-16</Field>
    
    <Field name="abnormal_interpretation_title">Normal</Field>
    <Field name="abnormal_interpretation_code_title">Normal</Field>
    <Field name="abnormal_interpretation_code_system">http://smartplatforms.org/terms/codes/LabResultInterpretation#</Field>
    <Field name="abnormal_interpretation_code_identifier">normal</Field>

    <Field name="accession_number">AC09205823577</Field>

    <Field name="name_title">Serum Sodium</Field>
    <Field name="name_code_title">Serum Sodium</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/LNC/</Field>
    <Field name="name_code_identifier">2951-2</Field>

    <Field name="status_title">Final results: complete and verified</Field>
    <Field name="status_code_title">Final results: complete and verified</Field>
    <Field name="status_code_system">http://smartplatforms.org/terms/codes/LabStatus#</Field>
    <Field name="status_code_identifier">final</Field>

    <Field name="notes">Blood sample appears to have hemolyzed</Field>

    <Field name="quantitative_result_non_critical_range_max_value">155</Field>
    <Field name="quantitative_result_non_critical_range_max_unit">mEq/L</Field>
    <Field name="quantitative_result_non_critical_range_min_value">120</Field>
    <Field name="quantitative_result_non_critical_range_min_unit">mEq/L</Field>

    <Field name="quantitative_result_normal_range_max_value">145</Field>
    <Field name="quantitative_result_normal_range_max_unit">mEq/L</Field>
    <Field name="quantitative_result_normal_range_min_value">135</Field>
    <Field name="quantitative_result_normal_range_min_unit">mEq/L</Field>

    <Field name="quantitative_result_value_value">140</Field> 
    <Field name="quantitative_result_value_unit">mEq/L</Field>
  </Model>
</Models>
""",
]

TEST_LABS = report_content_to_test_docs(_TEST_LABS)

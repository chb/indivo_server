from base import report_content_to_test_docs

_TEST_ALLERGIES_INVALID = [
    # an allergy with the wrong schema, should trigger a validation error
    """
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Allergy">
    <Field name="allergic_reaction_code_title">Anaphylaxis</Field>
    <Field name="allergic_reaction_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="allergic_reaction_code_identifier">39579001</Field>
    <Field name="category_code_title">Drug allergy</Field>
    <Field name="category_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="category_code_identifier">416098002</Field>
    <Field name="drug_class_allergen_code_title">Sulfonamide Antibacterial</Field>
    <Field name="drug_class_allergen_code_system">http://purl.bioontology.org/ontology/NDFRT/</Field>
    <Field name="drug_class_allergen_code_identifier">N0000175503</Field>
    <Field name="severity_code_title">Severe</Field>
    <Field name="severity_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="severity_code_identifier">24484000</Field>
    <Monkey name="woahthere">THIS SHOULDN'T BE THERE</Monkey>
  </Model>
</Models>
""",
]

_TEST_ALLERGIES = [
    """
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Allergy">
    <Field name="allergic_reaction_code_title">Anaphylaxis</Field>
    <Field name="allergic_reaction_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="allergic_reaction_code_identifier">39579001</Field>
    <Field name="category_code_title">Drug allergy</Field>
    <Field name="category_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="category_code_identifier">416098002</Field>
    <Field name="drug_class_allergen_code_title">Sulfonamide Antibacterial</Field>
    <Field name="drug_class_allergen_code_system">http://purl.bioontology.org/ontology/NDFRT/</Field>
    <Field name="drug_class_allergen_code_identifier">N0000175503</Field>
    <Field name="severity_code_title">Severe</Field>
    <Field name="severity_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="severity_code_identifier">24484000</Field>
  </Model>
</Models>
""",
"""
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="Allergy">
    <Field name="allergic_reaction_code_title">Anaphylaxis</Field>
    <Field name="allergic_reaction_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="allergic_reaction_code_identifier">39579001</Field>
    <Field name="category_code_title">Drug allergy</Field>
    <Field name="category_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="category_code_identifier">416098002</Field>
    <Field name="drug_allergen_code_title">Cephalexin</Field>
    <Field name="drug_allergen_code_system">http://purl.bioontology.org/ontology/RXNORM/</Field>
    <Field name="drug_allergen_code_identifier">2231</Field>
    <Field name="severity_code_title">Severe</Field>
    <Field name="severity_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="severity_code_identifier">24484000</Field>
  </Model>
</Models>
""",
]

_TEST_ALLERGY_EXCLUSIONS = [
    """
<Models xmlns="http://indivo.org/vocab/xml/documents#">
  <Model name="AllergyExclusion">
    <Field name="name_code_title">No known food allergy</Field>
    <Field name="name_code_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="name_code_identifier">429625007</Field>
  </Model>
</Models>
""",
]

TEST_ALLERGIES_INVALID = report_content_to_test_docs(_TEST_ALLERGIES_INVALID)
TEST_ALLERGIES = report_content_to_test_docs(_TEST_ALLERGIES)
TEST_ALLERGY_EXCLUSIONS = report_content_to_test_docs(_TEST_ALLERGY_EXCLUSIONS)

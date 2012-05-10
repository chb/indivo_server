from base import report_content_to_test_docs

_TEST_ALLERGIES_INVALID = [
    # an allergy with the wrong schema, should trigger a validation error
    """
<Models xmlns='http://indivo.org/vocab/xml/documents#'>
  <Model name="Allergy">
    <Field name="allergic_reaction_title">Anaphylaxis</Field>
    <Field name="allergic_reaction_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="allergic_reaction_identifier">39579001</Field>
    <Field name="category_title">Drug allergy</Field>
    <Field name="category_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="category_identifier">416098002</Field>
    <Field name="drug_class_allergen_title">Sulfonamide Antibacterial</Field>
    <Field name="drug_class_allergen_system">http://purl.bioontology.org/ontology/NDFRT/</Field>
    <Field name="drug_class_allergen_identifier">N0000175503</Field>
    <Field name="severity_title">Severe</Field>
    <Field name="severity_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="severity_identifier">24484000</Field>
    <Monkey name="woahthere">THIS SHOULDN'T BE THERE</Monkey>
  </Model>
</Models>
""",
]

_TEST_ALLERGIES = [
    """
<Models xmlns='http://indivo.org/vocab/xml/documents#'>
  <Model name="Allergy">
    <Field name="allergic_reaction_title">Anaphylaxis</Field>
    <Field name="allergic_reaction_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="allergic_reaction_identifier">39579001</Field>
    <Field name="category_title">Drug allergy</Field>
    <Field name="category_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="category_identifier">416098002</Field>
    <Field name="drug_class_allergen_title">Sulfonamide Antibacterial</Field>
    <Field name="drug_class_allergen_system">http://purl.bioontology.org/ontology/NDFRT/</Field>
    <Field name="drug_class_allergen_identifier">N0000175503</Field>
    <Field name="severity_title">Severe</Field>
    <Field name="severity_system">http://purl.bioontology.org/ontology/SNOMEDCT/</Field>
    <Field name="severity_identifier">24484000</Field>
  </Model>
</Models>
""",
]

TEST_ALLERGIES_INVALID = report_content_to_test_docs(_TEST_ALLERGIES_INVALID)
TEST_ALLERGIES = report_content_to_test_docs(_TEST_ALLERGIES)

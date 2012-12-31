from indivo.models import Allergy

allergy_fact = Allergy(
    allergic_reaction_title="Anaphylaxis",
    allergic_reaction_code_title="Anaphylaxis",
    allergic_reaction_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    allergic_reaction_code_identifier="39579001",
    category_title="Drug allergy",
    category_code_title="Drug allergy",
    category_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    category_code_identifier="416098002",
    drug_class_allergen_title="Sulfonamide Antibacterial",
    drug_class_allergen_code_title="Sulfonamide Antibacterial",
    drug_class_allergen_code_system="http://purl.bioontology.org/ontology/NDFRT/",
    drug_class_allergen_code_identifier="N0000175503",
    severity_title="Severe",
    severity_code_title="Severe",
    severity_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    severity_code_identifier="24484000",
    )

allergy_exclusion = AllergyExclusion(
    name_title="No known allergies",
    name_code_title="No known allergies",
    name_code_identifier="160244002",
    name_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
)

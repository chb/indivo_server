from indivo.models import Allergy

allergy_fact = Allergy(
    allergic_reaction_title="Anaphylaxis",
    allergic_reaction_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    allergic_reaction_identifier="39579001",
    category_title="Drug allergy",
    category_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    category_identifier="416098002",
    drug_class_allergen_title="Sulfonamide Antibacterial",
    drug_class_allergen_system="http://purl.bioontology.org/ontology/NDFRT/",
    drug_class_allergen_identifier="N0000175503",
    severity_title="Severe",
    severity_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    severity_identifier="24484000",
    )

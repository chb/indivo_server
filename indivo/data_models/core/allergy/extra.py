from indivo.data_models.options import DataModelOptions
from indivo.validators import ValueInSetValidator, ExactValueValidator

SNOMED = 'http://purl.bioontology.org/ontology/SNOMEDCT/'
RXNORM = 'http://purl.bioontology.org/ontology/RXNORM/'
NUI = 'http://purl.bioontology.org/ontology/NDFRT/'
UNII = 'http://fda.gov/UNII/'

VALID_CATEGORY_IDS = [
    '414285001', # Food allergy
    '426232007', # Environmental allergy
    '416098002', # Drug allergy
    '59037007',  # Drug intolerance
    '235719002', # Food intolerance
    ]

VALID_SEVERITY_IDS = [
    '255604002', # Mild
    '442452003', # Life Threatening
    '6736007',   # Moderate
    '399166001', # Fatal
    '24484000',  # Severe
]

VALID_EXCLUSION_IDS = [
    '160244002', # No known allergies
    '428607008', # No known environmental allergy
    '429625007', # No known food allergy
    '409137002', # No known history of drug allergy
]

class AllergyOptions(DataModelOptions):
    model_class_name = 'Allergy'
    field_validators = {
        'allergic_reaction_system': [ExactValueValidator(SNOMED)],
        'category_system': [ExactValueValidator(SNOMED)],
        'category_identifier': [ValueInSetValidator(VALID_CATEGORY_IDS)],
        'drug_allergen_system': [ExactValueValidator(RXNORM, nullable=True)],
        'drug_class_allergen_system': [ExactValueValidator(NUI, nullable=True)],
        'food_allergen_system': [ExactValueValidator(UNII, nullable=True)],
        'severity_system': [ExactValueValidator(SNOMED)],
        'severity_identifier': [ValueInSetValidator(VALID_SEVERITY_IDS)],
        }

class AllergyExclusionOptions(DataModelOptions):
    model_class_name = 'AllergyExclusion'
    field_validators = {
        'name_system': [ExactValueValidator(SNOMED)],
        'name_identifier': [ValueInSetValidator(VALID_EXCLUSION_IDS)],
        }

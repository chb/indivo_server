from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph
from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator

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

class AllergySerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addAllergyList(queryset.iterator())
        return graph.toRDF()

class AllergyOptions(DataModelOptions):
    model_class_name = 'Allergy'
    serializers = AllergySerializers
    field_validators = {
        'allergic_reaction_system': [ExactValueValidator(SNOMED)],
        'allergic_reaction_identifier': [NonNullValidator()],
        'allergic_reaction_title': [NonNullValidator()],
        'category_system': [ExactValueValidator(SNOMED)],
        'category_identifier': [ValueInSetValidator(VALID_CATEGORY_IDS)],
        'category_title': [NonNullValidator()],
        'drug_allergen_system': [ExactValueValidator(RXNORM, nullable=True)],
        'drug_class_allergen_system': [ExactValueValidator(NUI, nullable=True)],
        'food_allergen_system': [ExactValueValidator(UNII, nullable=True)],
        'severity_system': [ExactValueValidator(SNOMED)],
        'severity_identifier': [ValueInSetValidator(VALID_SEVERITY_IDS)],
        'severity_title': [NonNullValidator()],
        }

class AllergyExclusionSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addAllergyExclusions(queryset.iterator())
        return graph.toRDF()

class AllergyExclusionOptions(DataModelOptions):
    model_class_name = 'AllergyExclusion'
    serializers = AllergyExclusionSerializers
    field_validators = {
        'name_system': [ExactValueValidator(SNOMED)],
        'name_identifier': [ValueInSetValidator(VALID_EXCLUSION_IDS)],
        'name_title': [NonNullValidator()],
        }

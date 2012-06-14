from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph

IMM_STATUS_URI="http://smartplatforms.org/terms/codes/ImmunizationAdministrationStatus#"
IMM_PROD_URI="http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=cvx#"
IMM_CLASS_URI="http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=vg#"
IMM_REFUSE_URI="http://smartplatforms.org/terms/codes/ImmunizationRefusalReason#"

VALID_IMM_STATUSES = [
    'doseGiven',
    'notAdministered',
    'partialDose',
]

VALID_REFUSALS = [
    'vaccineUnavailable',
    'patientUndergoingDesensitizationTherapy',
    'notIndicatedPerGuidelines',
    'recentChemoOrRadiaton',
    'allergy',
    'providerDeferred',
    'documentedImmunityOrPreviousDisease',
    'previouslyVaccinated',
    'contraindicated',
    'patientOrParentRefused',
    'comfortMeasuresOnly',
    'possiblePriorAllergyOrReaction',
    'recentOrganOrStemCellTransplant',
]

class ImmunizationSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addImmunizationList(queryset.iterator())
        return graph.toRDF()

class ImmunizationOptions(DataModelOptions):
    model_class_name = 'Immunization'
    serializers = ImmunizationSerializers
    field_validators = {
        'date': [NonNullValidator()],
        'administration_status_system': [ExactValueValidator(IMM_STATUS_URI)],
        'administration_status_identifier': [ValueInSetValidator(VALID_IMM_STATUSES)],
        'administration_status_title': [NonNullValidator()],
        'product_class_system': [ExactValueValidator(IMM_CLASS_URI, nullable=True)],
        'product_class_2_system': [ExactValueValidator(IMM_CLASS_URI, nullable=True)],
        'product_name_system': [ExactValueValidator(IMM_PROD_URI)],
        'product_name_identifier': [NonNullValidator()],
        'product_name_title': [NonNullValidator()],
        'refusal_reason_system': [ExactValueValidator(IMM_REFUSE_URI, nullable=True)],
        'refusal_reason_identifier': [ValueInSetValidator(VALID_REFUSALS, nullable=True)],
        }

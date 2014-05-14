import logging

from django.forms import ModelForm

from .base import BaseRDFTransform
from .fulfillment import FulfillmentTransform

from indivo.models import Medication

logger = logging.getLogger(__name__)


class MedicationTransform(BaseRDFTransform):


    param_map = {
        'endDate': 'endDate',
        # 'fulfillment': 'fulfillments',                    # handled below as a related Fact
        'instructions': 'instructions',
        # 'provenance': 'provenance',                       # not currently stored in Indivo
        'startDate': 'startDate',
    }

    def to_facts(self, rdf_graph):
        """Extract Medication Facts from an RDF graph"""
        facts = []
        smart_medication_class = self.smart_class_dictionary['Medication']
        medication_params = self.smart_classes_to_params(rdf_graph, smart_medication_class)
        if medication_params:
            facts, sub_facts = self.params_to_facts(medication_params)
            facts.extend(sub_facts)

        return facts

    def params_to_facts(self, param_list):
        fill_transform = FulfillmentTransform()
        facts = []
        sub_facts = []
        for params in param_list:
            fact_params = {}

            # extract all simple fields
            fact_params.update(self.map_simple_fields(params, self.param_map))

            # drugName CodedValue
            fact_params.update(self.map_coded_value_field(params, 'drugName', 'name'))

            # quantity ValueAndUnit
            fact_params.update(self.map_value_and_unit_field(params, 'quantity', 'quantity'))

            # frequency ValueAndUnit
            fact_params.update(self.map_value_and_unit_field(params, 'frequency', 'frequency'))

            # provenance Code
            # Indivo currently only supports a single provenance value
            provenance = params.get('provenance')
            if provenance:
                provenance = provenance[0]
                fact_params['provenance_identifier'] = str(provenance.get('identifier'))
                fact_params['provenance_title'] = str(provenance.get('title'))
                fact_params['provenance_system'] = str(provenance.get('system'))

            # create Medication by form
            fact_form = MedicationForm(fact_params)
            import pdb; pdb.set_trace()
            medication = fact_form.save()

            # process related facts
            fills = params.get('fulfillment')
            if fills:
                fill_facts, fill_sub_facts = fill_transform.params_to_facts(fills)
                medication.fulfillments.add(*fill_facts)
                sub_facts.extend(fill_facts)
                sub_facts.extend(fill_sub_facts)

            facts.append(medication)

        logger.debug("Created %d Medications" % (len(facts)))
        return facts, sub_facts

class MedicationForm(ModelForm):
    class Meta:
        model = Medication
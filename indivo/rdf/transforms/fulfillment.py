import logging

from django.forms import ModelForm

from .base import BaseRDFTransform

from indivo.models import Fill

logger = logging.getLogger(__name__)


class FulfillmentTransform(BaseRDFTransform):


    param_map = {
        'date': 'date',
        'dispenseDaysSupply': 'dispenseDaysSupply',
        'pbm': 'pbm',
        }
    def to_facts(self, rdf_graph):
        """Extract Fulfillment Facts from an RDF graph"""
        facts = []
        smart_fulfillment_class = self.smart_class_dictionary['Fulfillment']
        fulfillment_params = self.smart_classes_to_params(rdf_graph, smart_fulfillment_class)
        if fulfillment_params:
            facts, sub_facts = self.params_to_facts(fulfillment_params)
            facts.extend(sub_facts)

        return facts

    def params_to_facts(self, param_list):
        facts = []
        sub_facts = []
        for params in param_list:
            fact_params = {}

            # simple fields
            fact_params.update(self.map_simple_fields(params, self.param_map))

            # quantity dispensed
            fact_params.update(self.map_value_and_unit_field(params, 'quantityDispensed', 'quantityDispensed'))

            # pharmacy
            fact_params.update(self.map_pharmacy_field(params, 'pharmacy', 'pharmacy'))

            # provider
            fact_params.update(self.map_provider_field(params, 'provider', 'provider'))

            fact_form = FulfillmentForm(fact_params)

            facts.append(fact_form.save())

        logger.debug("Created %d Fills" % (len(facts)))
        return facts, sub_facts

class FulfillmentForm(ModelForm):
        class Meta:
            model = Fill
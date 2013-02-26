import logging

from .base import BaseRDFTransform
from ..sparql import SMARTSPARQLQuery

from indivo.models import Medication

logger = logging.getLogger(__name__)

class MedicationTransform(BaseRDFTransform):


    def to_facts(self, rdf_graph):
        """Extract Medication Facts from an RDF graph"""

        query = SMARTSPARQLQuery('Medication')

        # drugName
        query.add_coded_value('drugName', 'name', optional=False)

        # instructions
        query.add_simple('instructions', optional=False)

        # startDate
        query.add_simple('startDate', optional=False)

        # endDate
        query.add_simple('endDate', optional=True)

        # frequency
        query.add_value_and_unit('frequency', optional=True)

        # quantity
        query.add_value_and_unit('quantity', optional=True)

        # query the graph
        query_string = query.generate_query_string()
        results = rdf_graph.query(query_string, initNs=query.NS)

        # transform to Facts
        fact_params = self._params_from_SPARQLQueryResult(results, query.fields)
        facts = []
        for params in fact_params:
            params.pop('model')
            facts.append(Medication(**params))

        logger.debug("Created %d Medications" % (len(facts)))

        return facts
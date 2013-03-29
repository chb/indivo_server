import logging
from lxml import etree
from rdflib import Graph

from .transforms import *

PARSE_MAP = {
    'Medication': MedicationTransform(),
    'Fulfillment': FulfillmentTransform(),
}

logger = logging.getLogger(__name__)

def parse(doc_etree):
    """parse RDF/XML into Facts"""

    # build an RDF graph from the RDF/XML
    g = Graph()
    try:
        g.parse(data=etree.tostring(doc_etree))
    except Exception:
        logger.exception("Failed to parse input to RDF Graph")
        return None

    # Find top level element type to transform  TODO: arbitrary designation, why not allow mixed elements?
    _smart_tag = lambda tag_name: "{%s}%s"%("http://smartplatforms.org/terms#", tag_name)
    for model_name in PARSE_MAP:
        elements = doc_etree.find(_smart_tag(model_name))
        if len(elements) > 0:
            return PARSE_MAP.get(model_name)(g)

    return None

from lxml import etree
from indivo.document_processing import BaseTransform
from indivo.rdf import parser

class Transform(BaseTransform):

    def to_facts(self, doc_etree):

        return parser.parse(doc_etree)

from indivo.document_processing import BaseTransform

INDIVO_DOC_NS = "{http://indivo.org/vocab/xml/documents#}"

class Transform(BaseTransform):

    def to_sdmx(self, doc_etree):

        # We already have SDMX, but it came in with
        # the indivo namespace, so we need to strip the NS
        for el in doc_etree.iter(tag="%s*"%INDIVO_DOC_NS):
            el.tag = el.tag.replace(INDIVO_DOC_NS, '')
        return doc_etree

from indivo.document_processing import BaseTransform
from lxml import etree

INDIVO_DOC_NS = "{http://indivo.org/vocab/xml/documents#}"

class Transform(BaseTransform):

    def to_sdmx(self, doc_etree):

        # We already have SDMX, but it came in with
        # the indivo namespace, so we need to strip the NS
        for el in doc_etree.iter(tag="%s*"%INDIVO_DOC_NS):
            el.tag = el.tag.replace(INDIVO_DOC_NS, '')

        # Look for a preprocessor for the SDMX transform, then call it
        for model_etree in doc_etree.iter(tag='Model'):
            model_name = model_etree.get('name')
            if model_name:
                try:
                    model_class = getattr(__import__('indivo.models', fromlist=[model_name]), model_name, None)
                except ImportError:
                    model_class = None

            if model_class:
                func = getattr(model_class, 'to_sdmx', None)
                if func:
                    ret = func(model_etree)
                    if isinstance(ret, etree._ElementTree):
                        doc_etree[doc_etree.index(model_etree)] = ret

        return doc_etree

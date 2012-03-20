from indivo.document_processing import BaseTransform
from indivo.models import Allergy
from lxml import etree
from StringIO import StringIO

NS = "http://indivo.org/vocab/xml/documents#"

SDMJ_TEMPLATE = '''
{ "__modelname__": "Allergy",
  "date_diagnosed": "%(date_diagnosed)s",
  "diagnosed_by": "%(diagnosed_by)s",
  "allergen_type": "%(allergen_type)s",
  "allergen_type_type": "%(allergen_type_type)s",
  "allergen_type_value": "%(allergen_type_value)s",
  "allergen_type_abbrev": "%(allergen_type_abbrev)s",
  "allergen_name": "%(allergen_name)s",
  "allergen_name_type": "%(allergen_name_type)s",
  "allergen_name_value": "%(allergen_name_value)s",
  "allergen_name_abbrev": "%(allergen_name_abbrev)s",
  "reaction": "%(reaction)s",
  "specifics": "%(specifics)s"
}
'''

SDMX_TEMPLATE = '''
<Models>
  <Model name="Allergy">
    <date_diagnosed>%(date_diagnosed)s</date_diagnosed>
    <diagnosed_by>%(diagnosed_by)s</diagnosed_by>
    <allergen_type>%(allergen_type)s</allergen_type>
    <allergen_type_type>%(allergen_type_type)s</allergen_type_type>
    <allergen_type_value>%(allergen_type_value)s</allergen_type_value>
    <allergen_type_abbrev>%(allergen_type_abbrev)s</allergen_type_abbrev>
    <allergen_name>%(allergen_name)s</allergen_name>
    <allergen_name_type>%(allergen_name_type)s</allergen_name_type>
    <allergen_name_value>%(allergen_name_value)s</allergen_name_value>
    <allergen_name_abbrev>%(allergen_name_abbrev)s</allergen_name_abbrev>
    <reaction>%(reaction)s</reaction>
    <specifics>%(specifics)s</specifics>
  </Model>
</Models>
'''

class Transform(BaseTransform):

    # NOTE: We define to_facts(), to_sdmj(), and to_sdmx() as an EXAMPLE ONLY.
    # When implementing Transforms, any one of these methods will suffice.

    def to_facts(self, doc_etree):
        args = self._get_data(doc_etree)

        # Create the fact and return it
        # Note: This method must return a list
        return [Allergy(**args)]
        
    def to_sdmj(self, doc_etree):
        args = self._get_data(doc_etree)
        return SDMJ_TEMPLATE%args

    def to_sdmx(self, doc_etree):
        args = self._get_data(doc_etree)
        return etree.parse(StringIO(SDMX_TEMPLATE%args))

    def _tag(self, tagname):
        return "{%s}%s"%(NS, tagname)

    def _get_data(self, doc_etree):
        """ Parse the etree and return a dict of key-value pairs for object construction. """
        ret = {}
        _t = self._tag

        # Get the date_diagnosed
        ret['date_diagnosed'] = doc_etree.findtext(_t('dateDiagnosed'))
        
        # Get the diagnosed_by
        ret['diagnosed_by'] = doc_etree.findtext(_t('diagnosedBy'))

        # Get the allergen_type, allergen_type_type, allergen_type_value, allergen_type_abbrev
        allergen_type_node = doc_etree.find(_t('allergen')).find(_t('type'))
        ret['allergen_type'] = allergen_type_node.text
        ret['allergen_type_type'] = allergen_type_node.get('type')
        ret['allergen_type_value'] = allergen_type_node.get('value')
        ret['allergen_type_abbrev'] = allergen_type_node.get('abbrev')

        # Get the allergen_name, allergen_name_name, allergen_name_value, allergen_name_abbrev
        allergen_name_node = doc_etree.find(_t('allergen')).find(_t('name'))
        ret['allergen_name'] = allergen_name_node.text
        ret['allergen_name_type'] = allergen_name_node.get('type')
        ret['allergen_name_value'] = allergen_name_node.get('value')
        ret['allergen_name_abbrev'] = allergen_name_node.get('abbrev')

        # Get the Comments
        ret['reaction'] = doc_etree.findtext(_t('reaction'))

        # Get the Diagnosed_by
        ret['specifics'] = doc_etree.findtext(_t('specifics'))
        
        return ret

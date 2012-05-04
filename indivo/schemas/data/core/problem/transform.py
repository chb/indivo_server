from indivo.document_processing import BaseTransform
from indivo.models import Problem

class Transform(BaseTransform):
    def to_fact(self, doc_etree):
        args = self._get_data(doc_etree)

        # Create the fact and return it
        # Note: This method must return a list
        return [Problem(**args)]
        
    def to_sdmj(self, doc_etree):
        pass

    def to_sdmx(self, doc_etree):
        pass

    def _get_data(self, doc_etree):
        """ Parse the etree and return a dict of key-value pairs for object construction. """
        ret = {}

        # Get the date_onset
        ret['startDate'] = doc_etree.findText('dateOnset')
        
        # Get the date_resolution
        ret['endDate'] = doc_etree.findText('dateResolution')

        # Get the name, name_type, name_value, name_abbrev
        name_node = doc_etree.find('name')
        ret['name_title'] = name_node.text
        ret['name_system'] = name_node.get('type')
        ret['name_identifier'] = name_node.get('value')

        # Get the notes
        ret['notes'] = doc_etree.findText('comments')

        return ret

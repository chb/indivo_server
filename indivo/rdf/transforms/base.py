import logging

from rdflib.exceptions import UniquenessError
from smart_common.rdf_tools.rdf_ontology import api_types

from indivo.document_processing import BaseTransform

logger = logging.getLogger(__name__)

class BaseRDFTransform(BaseTransform):
    """ Base class for SMART RDF transforms."""


    smart_class_dictionary = {t.name:t for t in api_types}

    def smart_class_to_params(self, graph, subject, klass, base=''):
        """
        Extract out a property:value dictionary representing a specific instance of a SMART_Class in the Graph

        :param graph: RDF Graph to search
        :param subject: RDF subject to extract
        :param klass: SMART_Class to extract the subject as
        :param base: prefix string for keys
        :return: property:value dictionary representing the subject
        """

        if not subject:
            # empty params if no subject
            return {}

        params = {}
        if base:
            base += '_'

        # simple data properties
        for klass_property in klass.data_properties:
            if klass_property.multiple_cardinality:
                # multi-valued
                values = []
                objects = graph.objects(subject=subject, predicate=klass_property.uri)
                for value in objects:
                    values.append(value)
                if values:
                    params['%s%s' % (base, klass_property.name)] = values
            else:
                # single valued
                try:
                    value = graph.value(subject=subject, predicate=klass_property.uri, any=False)
                    if value:
                        params['%s%s' % (base, klass_property.name)] = value
                except UniquenessError:
                    logger.warn("Expecting single value for data property", exc_info=1)
                    raise

        # object properties
        for klass_property in klass.object_properties:
            if klass_property.object_property_inverses.has_key(klass_property.uri):
                # don't follow links back  TODO: make sure this is defined well enough in OWL to protect against blowing the stack
                continue
            elif klass_property.multiple_cardinality:
                # multi-instance
                property_subjects = graph.objects(subject=subject, predicate=klass_property.uri)
                sub_params = []
                property_klass = klass_property.to_class
                for property_subject in property_subjects:
                    sub_params.append(self.smart_class_to_params(graph, property_subject, property_klass))
                params['%s%s' % (base, klass_property.name)] = sub_params
            else:
                # single instance
                property_subject = graph.value(subject=subject, predicate=klass_property.uri)
                if property_subject:
                    property_klass = klass_property.to_class
                    property_params = self.smart_class_to_params(graph, property_subject, property_klass, base=(base + klass_property.name))
                    if property_params:
                        params.update(property_params)
                    else:
                        # not in the graph, so use the URIRef
                        resource = graph.value(subject=subject, predicate=klass_property.uri)
                        params['%s%s' % (base, klass_property.name)] = resource

        return params

    def smart_classes_to_params(self, graph, klass):
        """
        Extract out a list of property:value dictionaries for all instances of a SMART_Class in the Graph

        :param graph: RDF Graph to search
        :param klass: SMART_Class to search for
        :return: list of property:value dictionaries for all instances of type klass found
        """
        params = []
        subjects = graph.subjects(None, klass.uri)
        for subject in subjects:
            params.append(self.smart_class_to_params(graph, subject, klass))

        return params

    def map_simple_fields(self, params, mappings):
        """
        Map matching params to new keys

        :param params: dictionary of params to try mapping
        :param mappings: dictionary of key:new_key mappings
        :return: dictionary of mapped params
        """
        return {mappings[key]: str(params[key]) for key in params if mappings.has_key(key)}

    def map_code_field(self, params, from_field, to_field):
        """
        Convenience method for mapping a :py:class:`~indivo.fields.CodeField`

        :param params: dictionary of params to ty mapping
        :param from_field: value for {from_field} replacement
        :param to_field: value for {to_field} replacement
        :return: dictionary of mapped params
        """
        mappings = {
            '{from_field}identifier': '{to_field}identifier',
            '{from_field}system': '{to_field}system',
            '{from_field}title': '{to_field}title',
            }

        mappings = self._format_mappings(mappings, from_field, to_field)
        mapped_params = self.map_simple_fields(params, mappings)

        return mapped_params

    def map_coded_value_field(self, params, from_field, to_field):
        """
        Convenience method for mapping a `~indivo.fields.CodedValueField`

        :param params: dictionary of params to ty mapping
        :param from_field: value for {from_field} replacement
        :param to_field: value for {to_field} replacement
        :return: dictionary of mapped params
        """
        mappings = {
            '{from_field}title': '{to_field}title',
            }

        mappings = self._format_mappings(mappings, from_field, to_field)
        mapped_params = self.map_simple_fields(params, mappings)

        # code
        mapped_params.update(self.map_code_field(params, '%s_code'%(from_field), '%s_code'%(to_field)))

        # we currently only store a single provenance in Indivo for CodedValueField
        name_provenance = params.get('%s_provenance' % from_field)
        if name_provenance:
            name_provenance = name_provenance[0]
            mapped_params['%s_provenance_source_code' % to_field] = str(name_provenance.get('sourceCode'))
            mapped_params['%s_provenance_title' % to_field] = str(name_provenance.get('title'))

            # TODO: For now we handle a full TranslationFidelity code or URIRef for translation fidelity input, but we only output the URIRef
            # figure out if we have the full translation fidelity, or just the URIRef
            fidelity_system = name_provenance.get('translationFidelity_system', None)
            if fidelity_system:
                mapped_params['%s_provenance_translation_fidelity' % to_field] = str(fidelity_system + name_provenance.get('translationFidelity_identifier'))
            else:
                # we just have the URIRef
                mapped_params['%s_provenance_translation_fidelity' % to_field] = str(name_provenance.get('translationFidelity'))

        return mapped_params

    def map_pharmacy_field(self, params, from_field, to_field):
        """
        Convenience method for mapping a `~indivo.fields.PharmacyField`

        :param params: dictionary of params to ty mapping
        :param from_field: value for {from_field} replacement
        :param to_field: value for {to_field} replacement
        :return: dictionary of mapped params
        """
        mappings = {
            '{from_field}ncpdpId': '{to_field}ncpdpid',
            '{from_field}organization-name': '{to_field}org',
        }

        mappings = self._format_mappings(mappings, from_field, to_field)
        mapped_params = self.map_simple_fields(params, mappings)
        # address
        mapped_params.update(self.map_address_field(params, '%s_adr'%(from_field), '%s_adr'%(to_field)))

        return mapped_params

    def map_provider_field(self, params, from_field, to_field):
        """
        Convenience method for mapping a `~indivo.fields.ProviderField`

        :param params: dictionary of params to ty mapping
        :param from_field: value for {from_field} replacement
        :param to_field: value for {to_field} replacement
        :return: dictionary of mapped params
        """
        mappings = {
            '{from_field}deaNumber': '{to_field}dea_number',
            '{from_field}ethnicity': '{to_field}ethnicity',
            '{from_field}npiNumber': '{to_field}npi_number',
            '{from_field}preferredLanguage': '{to_field}preferred_language',
            '{from_field}race': '{to_field}race',
            '{from_field}bday': '{to_field}bday',
            '{from_field}gender': '{to_field}gender',
        }

        mappings = self._format_mappings(mappings, from_field, to_field)
        mapped_params = self.map_simple_fields(params, mappings)

        # we only store a single email
        email = params.get('%s_email' % from_field)
        if email:
            email = email[0]
            mapped_params['%s_email' % to_field] = str(email)

        # we only store up to two telephone numbers
        telephone_list = params.get('%s_tel' % from_field)
        if telephone_list:
            telephone_1 = telephone_list[0]
            mapped_params['%s_tel_1_number' % to_field] = str(telephone_1.get('value'))
            if len(telephone_list) > 1:
                telephone_2 = telephone_list[1]
                mapped_params['%s_tel_2_number' % to_field] = str(telephone_2.get('value'))

        # we only store a single address
        address = params.get('%s_adr' % from_field)
        if address:
            address = address[0]
            mapped_params.update(self.map_address_field(address, '', '%s_adr'%(to_field)))

        # name
        mapped_params.update(self.map_name_field(params, '%s_n'%(from_field), '%s_name'%(to_field)))

        return mapped_params

    def map_value_and_unit_field(self, params, from_field, to_field):
        """
        Convenience method for mapping a `~indivo.fields.ValueAndUnitField`

        :param params: dictionary of params to ty mapping
        :param from_field: value for {from_field} replacement
        :param to_field: value for {to_field} replacement
        :return: dictionary of mapped params
        """
        mappings = {
            '{from_field}value': '{to_field}value',
            '{from_field}unit': '{to_field}unit',
        }

        mappings = self._format_mappings(mappings, from_field, to_field)
        mapped_params = self.map_simple_fields(params, mappings)
        return mapped_params

    def map_address_field(self, params, from_field, to_field):
        """
        Convenience method for mapping an `~indivo.fields.AddressField`

        :param params: dictionary of params to ty mapping
        :param from_field: value for {from_field} replacement
        :param to_field: value for {to_field} replacement
        :return: dictionary of mapped params
        """
        mappings= {
            '{from_field}country-name': '{to_field}country',
            # '{from_field}extended-address': '{to_field}extended-address',   # not supported by Indivo
            '{from_field}locality': '{to_field}city',
            '{from_field}postal-code': '{to_field}postalcode',
            '{from_field}region': '{to_field}region',
            '{from_field}street-address': '{to_field}street',
            }

        mappings = self._format_mappings(mappings, from_field, to_field)
        mapped_params = self.map_simple_fields(params, mappings)
        return mapped_params

    def map_name_field(self, params, from_field, to_field):
        """
        Convenience method for mapping a `~indivo.fields.NameField`

        :param params: dictionary of params to ty mapping
        :param from_field: value for {from_field} replacement
        :param to_field: value for {to_field} replacement
        :return: dictionary of mapped params
        """
        mappings= {
            '{from_field}family-name': '{to_field}family',
            '{from_field}given-name': '{to_field}given',
            }

        mappings = self._format_mappings(mappings, from_field, to_field)
        mapped_params = self.map_simple_fields(params, mappings)

        # support only single values of these
        additional_name = params.get('%s_additional-name'%from_field)
        if additional_name:
            mapped_params['%s_middle' % to_field] = str(additional_name[0])

        name_prefix = params.get('%s_honorific-prefix'%from_field)
        if name_prefix:
            mapped_params['%s_prefix' % to_field] = str(name_prefix[0])

        name_suffix = params.get('%s_honorific-suffix'%from_field)
        if name_suffix:
            mapped_params['%s_suffix' % to_field] = str(name_suffix[0])

        return mapped_params

    def _format_mappings(self, mappings, from_field, to_field):
        """
        Convenience method for formatting mappings with {from_filed} and {to_field} replacement fields in the key/value
        pairs

        :param mappings: dictionary to format
        :param from_field: substitution value for {from_field}
        :param to_field: substitution value for {to_field}
        :return: dictionary of formatted parameters
        """
        from_field = from_field + '_' if from_field else ''
        to_field = to_field + '_' if to_field else ''
        return {key.format(from_field=from_field): value.format(to_field=to_field) for key, value in mappings.iteritems() }
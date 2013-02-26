from .rdf import RDF, SP, SPCODE, DCTERMS

class SMARTSPARQLQuery(object):
    """Convenience class for constructing SMART RDF SPARQL queries"""
    NS = {'rdf':RDF, 'sp':SP, 'spcode':SPCODE, 'dcterms':DCTERMS}

    def __init__(self, model_name):
        """
        Initialize a SMARTSPARQLQuery

        :param model_name: SMART Data Model to query for
        """
        self.queries = []
        self.optional_blocks = []
        self.fields = ['model']
        self.model_name = model_name
        self._add_as_required(["?model rdf:type sp:%s . " % self.model_name])

    def _add_fields(self, fields):
        self.fields.extend(fields)

    def _add_as_required(self, queries):
        self.queries.extend(queries)

    def _add_as_optional_block(self, block):
        self.optional_blocks.append(block)

    def generate_query_string(self):
        """Return a SPARQL query string for this query"""
        select = "SELECT ?%s" % (" ?".join(self.fields))
        required = "\n".join(self.queries)
        optional = ""
        if len(self.optional_blocks) > 0:
            optional = [o.to_query_string() for o in self.optional_blocks]
            optional = "\n".join(optional)

        where = "WHERE { %s %s}" % (required, optional)

        query = "\n".join([select, where])

        return query

    def add_simple(self, field_name, optional=False):
        """Add a simple field to the query"""
        fields = [field_name]
        queries = [("?model sp:%s ?%s ." % (field_name, field_name))]

        self._add_fields(fields)
        if optional:
            optional_block = SPARQLOptionalBlock(queries)
            self._add_as_optional_block(optional_block)
        else:
            self._add_as_required(queries)

        return fields, queries

    def add_value_and_unit(self, field_name, optional=False):
        """Add a ValueAndUnit field to the query"""
        queries = ["?model sp:{field_name} ?{field_name}_value_and_unit .",
                   "?{field_name}_value_and_unit sp:value ?{field_name}_value ."
                   "?{field_name}_value_and_unit sp:unit ?{field_name}_unit ."
        ]
        queries = [q.format(field_name=field_name) for q in queries]
        fields = ["%s_value"%field_name, "%s_unit"%field_name]

        self._add_fields(fields)
        if optional:
            optional_block = SPARQLOptionalBlock(queries)
            self._add_as_optional_block(optional_block)
        else:
            self._add_as_required(queries)

        # TODO: what do we want back from this?
        return fields, queries

    def add_coded_value(self, element_name, field_name, optional=False):
        """Add a CodedValue field to the query"""
        required_queries = [
            "?model sp:{element_name} ?{element_name}_coded_value .",
            "?{element_name}_coded_value dcterms:title ?{field_name}_title .",
            "?{element_name}_coded_value sp:code ?{element_name}_code .",
            "?{element_name}_code dcterms:title ?{field_name}_code_title .",
            "?{element_name}_code dcterms:identifier ?{field_name}_code_identifier .",
            "?{element_name}_code sp:system ?{field_name}_code_system ."
        ]

        optional_queries = [
            "?{element_name}_coded_value sp:provenance ?{element_name}_provenance .",
            "?{element_name}_provenance dcterms:title ?{field_name}_provenance_title .",
            "?{element_name}_provenance sp:sourceCode ?{field_name}_provenance_source_code .",
        ]

        nested_optional_queries = [
            "?{element_name}_provenance sp:translationFidelity ?{field_name}_provenance_translation_fidelity .",
        ]

        def _format(query):
            return query.format(element_name=element_name, field_name=field_name)

        required_queries = [_format(q) for q in required_queries]
        optional_queries = [_format(q) for q in optional_queries]
        nested_optional_queries = [_format(q) for q in nested_optional_queries]

        fields = [
            "{field_name}_title",
            "{field_name}_code_title",
            "{field_name}_code_identifier",
            "{field_name}_code_system",
            "{field_name}_provenance_title",
            "{field_name}_provenance_source_code",
            "{field_name}_provenance_translation_fidelity"
        ]

        fields = [_format(f) for f in fields]

        self._add_fields(fields)

        # add in always optional queries
        optional_block = SPARQLOptionalBlock(optional_queries)
        nested_optional_block = SPARQLOptionalBlock(nested_optional_queries)
        optional_block.add_nested_block(nested_optional_block)

        # required_fields might be optional
        if optional:
            optional_block.add_queries(required_queries)
            self._add_as_optional_block(optional_block)
        else:
            self._add_as_required(required_queries)

        self._add_as_optional_block(optional_block)

        return True

class SPARQLOptionalBlock(object):
    """Represent OPTIONAL SPARQL blocks"""

    def __init__(self, queries):
        self.queries = queries
        self.children = []

    def add_nested_block(self, block):
        self.children.append(block)

    def add_queries(self, queries):
        self.queries.extend(queries)

    def to_query_string(self):

        if self.queries or self.children:
            nested_queries = [n.to_query_string() for n in self.children]
            return "Optional {\n" + "\n".join(self.queries) + "\n" + ("\n".join(nested_queries) if self.children else "") + "\n}"
        else:
            return ""
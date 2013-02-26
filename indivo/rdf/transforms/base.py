from itertools import izip

from indivo.document_processing import BaseTransform

class BaseRDFTransform(BaseTransform):
    """ Base class for RDF transforms."""

    def _params_from_SPARQLQueryResult(self, results, fields, include_NONE=False):
        """
        Turn SPARQLQueryResult objects into parameter dictionaries for building models

        :param results: SPARQLQueryResult to transform
        :param fields: ordered list of keys for the dictionary
        :param include_NONE: keep None values and output as 'None'

        Each row of a SPARQLQueryResult is zipped up with passed in field names, creating a parameter dictionary
        suitable for object creation.  String representations of each row are used for the values, with the option
        to control whether None is output as the string 'None'
        """
        fact_params = []
        seen = set([])
        for row in results:
            # build a dictionary of field names to values
            params = dict(izip(fields, row))
            if (not include_NONE):
                # filter out any None values if requested
                params = {key: str(params[key]) for key in params if params[key]}
            fact_params.append(params)
            seen.add(params.get("model", None))

        if len(fact_params) > len(seen):
            raise Exception("RDF parsed into ambiguous Fact objects")

        return fact_params
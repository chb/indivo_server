"""
A quick utility to validate an XML doc against a schema

Ben Adida
ben.adida@childrens
2009-06-26

python validate_xml_with_schema.py schema.xsd doc.xml
"""

import sys
from lxml import etree

def validate_docs(xsd_path, xml_paths, verbose=1):
    with open(xsd_path, "r") as schema_file:
        schema = etree.XMLSchema(etree.parse(schema_file))

    for xml_path in xml_paths:
        with open(xml_path, "r") as xml_file:
            doc = etree.parse(xml_file)
        
        output = 'Validating %s against %s...      '%(xml_path, xsd_path)
        if schema.validate(doc):
            output += "ok"
        else:
            log = schema.error_log
            error = log.last_error
            output += str(error)
        
        if verbose:
            print output

if __name__ == '__main__':
    schema_path = sys.argv[1]
    xml_paths = sys.argv[2:]
    validate_docs(schema_path, xml_paths)

"""
A utility to validate multiple example XML docs against a schema

Daniel Haas
daniel.haas@childrens.harvard.edu
2012-03-02

python validate.py schema_dir_1 schema_dir_2 ... -vVerbosity
OR
python validate.py # Validates everything

"""

import sys, os
from lxml import etree
import glob

DEFAULT_SCHEMA_DIRS = [
    '../metadata',
    '../data/core',
    '../data/contrib',
    '../data/output',
]

def discover_schemas(schema_dirs):
    ret = []
    for schema_dir in schema_dirs:
        full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), schema_dir)
        for entry in os.listdir(full_path):
            schema_path = os.path.join(full_path, entry)
            if os.path.isdir(schema_path) and glob.glob(os.path.join(schema_path, '*.xsd')):
                ret.append(schema_path)
    
    return ret

def get_examples(schema_dir):
    return glob.glob(os.path.join(schema_dir, '*.xml'))

def get_xsd(schema_dir):
    try:
        return glob.glob(os.path.join(schema_dir, '*.xsd'))[0]
    except IndexError:
        raise ValueError('Schema directory %s doesn\'t contain a valid XSD file'%schema_dir)

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
    schema_paths = []
    verbose = 1
    for arg in sys.argv[1:]:
        if arg.startswith('-v'):
            verbose = int(arg[2:])
        else:
            schema_paths.append(arg)
    
    if not schema_paths:
        schema_paths = discover_schemas(DEFAULT_SCHEMA_DIRS)

    for schema_path in schema_paths:
        xsd_path = get_xsd(schema_path)
        xml_paths = get_examples(schema_path)
        validate_docs(xsd_path, xml_paths, verbose)

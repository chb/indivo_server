import os
import sys
from xml.dom import minidom
import datasections

def import_data(verbosity=True):
  bf_prefix = ''
  if os.path.dirname(__file__):
    bf_prefix = os.path.dirname(__file__) + '/'
    data_file  = bf_prefix + 'indivo_data.xml'

  if os.path.isfile(data_file):
    f = open(data_file)
    lines = []
    for line in f:
      lines.append(line.strip())
    dom = minidom.parseString(''.join(lines))
    for root in dom.childNodes:
      # Make sure to pull in required info first
      # This is hack, but the required stuff shouldn't
      # really be in the data file anyways.
      
      # Required info is auth_systems, status_names, document_schemas
      req_secs = ['auth_systems', 'status_names', 'document_schemas']

      for section in root.childNodes:
        if section and getattr(section, 'nodeName', None) in req_secs:
          import_section(section, verbosity)

      # Now import the others
      for section in root.childNodes:
        if section and getattr(section, 'nodeName', None) not in req_secs:
          import_section(section, verbosity)
  else:
    raise ValueError("No indivo_data.xml file found")

def import_section(section, verbosity):
  try:
    # Note the nodeName, className and fileName relationship
    if hasattr(section, 'nodeName'):
      if hasattr(datasections, section.nodeName):
        class_name = section.nodeName.capitalize()
        seclib = getattr(datasections, section.nodeName)
        if hasattr(seclib, class_name):
          getattr(seclib, class_name)(section, verbosity)
  except ImportError:
    pass


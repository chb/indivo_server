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
      for section in root.childNodes:
        try:
          # Note the nodeName, className and fileName relationship
          if section and hasattr(section, 'nodeName'):
            if hasattr(datasections, section.nodeName):
              class_name = section.nodeName.capitalize()
              seclib = getattr(datasections, section.nodeName)
              if hasattr(seclib, class_name):
                getattr(seclib, class_name)(section, verbosity)
        except ImportError:
          pass
  else:
    raise ValueError("No indivo_data.xml file found")

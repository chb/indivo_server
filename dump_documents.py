"""
A script to dump documents for records created by
indivo-connector
"""

##
## DJANGO SETUP
##
import string
import os
import sys
from indivo.models import *
from xml.etree import ElementTree

os.environ['DJANGO_SETTINGS_MODULE'] = 'indivo.settings'
##
## constants
##

INFO = """<patient>
  <last_name>%s</last_name>
  <first_names>%s</first_names>
  <mrn>%s</mrn>
  <confirmation_code>%s</confirmation_code>
</patient>"""
##
## now the script
##

def dump_documents():
  out_dir = sys.argv[1]

  # go through the patients
  p = Principal.objects.get(email='indivoconnector-admin@apps.indivo.org')

  records = Record.objects.filter(creator=p)
  print "%s records" % len(records)

  PREFIX = "http://indivo.org/vocab/xml/documents#"

  for i, record in enumerate(records):
    record_dir = out_dir + ("/patient_%s" % i)

    # make the directory
    os.mkdir(record_dir)

    # we need basic info, first name, last name
    contact = ElementTree.fromstring(record.contact.content)
    last_name = contact.findtext("{%s}name/{%s}familyName" % (PREFIX,PREFIX))
    first_name = contact.findtext("{%s}name/{%s}givenName" % (PREFIX,PREFIX))
  
    # generate a random MRN
    mrn = "%s-%s-%s" % (utils.random_string(3, choices=string.digits),
                        utils.random_string(3, choices=string.digits),
                        utils.random_string(3, choices=string.digits))

    confirmation_code = utils.random_string(3, choices=string.digits)

    info = INFO % (last_name, first_name, mrn, confirmation_code)

    info_file = open(record_dir + "/info.xml", "w")
    info_file.write(info)
    info_file.close()

    # go through documents
    for i, doc in enumerate([r for r in record.documents.all()]):
      doc_file = open(record_dir + "/doc_" + str(i), "w")
      doc_file.write(doc.content)
      doc_file.close()

if __name__ == '__main__':
  dump_documents()

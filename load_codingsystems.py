"""
Driver for coding system loading
"""

from django.core.management import setup_environ
import settings
setup_environ(settings)

from codingsystems.data import snomed, loinc, rxterms, hl7vaccines

snomed.create_and_load_from('codingsystems/data/complete/SNOMEDCT_CORE_SUBSET_200911_utf8.txt')
loinc.create_and_load_from('codingsystems/data/complete/LOINCDB.TXT')
rxterms.create_and_load_from('codingsystems/data/complete/RxTerms201005.txt')
hl7vaccines.create_and_load_from('codingsystems/data/complete/HL7_V3_VACCINES.txt')

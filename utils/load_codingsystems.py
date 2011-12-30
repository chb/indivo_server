"""
Driver for coding system loading
"""

from codingsystems.data import snomed, loinc, rxterms, hl7vaccines

def load_codingsystems():
    snomed.create_and_load_from('codingsystems/data/complete/SNOMEDCT_CORE_SUBSET_200911_utf8.txt')
    loinc.create_and_load_from('codingsystems/data/complete/LOINCDB.TXT')
    rxterms.create_and_load_from('codingsystems/data/complete/RxTerms201005.txt')
    hl7vaccines.create_and_load_from('codingsystems/data/complete/HL7_V3_VACCINES.txt')
    
if __name__ == '__main__':
    load_codingsystems()

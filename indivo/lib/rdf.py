""" Utilities for generating RDF graphs.

Adapted from the `Smart Sample Data generator <https://github.com/chb/smart_sample_patients/blob/master/bin/generate.py>`_.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu

"""
from rdflib import ConjunctiveGraph, Namespace, BNode, Literal, RDF, URIRef

# Some constant strings:
SP_DEMOGRAPHICS = "http://smartplatforms.org/records/%s/demographics"
RXN_URI="http://purl.bioontology.org/ontology/RXNORM/%s"
NUI_URI="http://purl.bioontology.org/ontology/NDFRT/%s"
UNII_URI="http://fda.gov/UNII/%s"
SNOMED_URI="http://purl.bioontology.org/ontology/SNOMEDCT/%s"
LOINC_URI="http://purl.bioontology.org/ontology/LNC/%s"
MED_PROV_URI="http://smartplatforms.org/terms/codes/MedicationProvenance#%s"
ENC_TYPE_URI="http://smartplatforms.org/terms/codes/EncounterType#%s"
IMM_STATUS_URI="http://smartplatforms.org/terms/codes/ImmunizationAdministrationStatus#%s"
IMM_PROD_URI="http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=cvx#%s"
IMM_CLASS_URI="http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=vg#%s"
IMM_REFUSE_URI="http://smartplatforms.org/terms/codes/ImmunizationRefusalReason#%s"
INDIVO_RECORD_URI="http://indivo.org/records/%s"
INDIVO_VOCAB_URI="http://indivo.org/vocab/documents#%s"

# First Declare Name Spaces
SP = Namespace("http://smartplatforms.org/terms#")
SPCODE = Namespace("http://smartplatforms.org/terms/codes/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")
VCARD=Namespace("http://www.w3.org/2006/vcard/ns#")


class PatientGraph(object):
    """ Represents a patient's RDF graph"""

    def __init__(self, record):
        """Create an instance of a RDF graph for patient instance p""" 
        self.record=record
        
        # Create a RDF graph and namespaces:
        g = ConjunctiveGraph()
        self.g = g  # Keep a reference to this graph as an instance var
        
        # BindNamespaces to the graph:
        g.bind('rdfs', RDFS)
        g.bind('sp', SP)
        g.bind('spcode', SPCODE)
        g.bind('dc', DC)
        g.bind('dcterms', DCTERMS)
        g.bind('foaf', FOAF)
        g.bind('v', VCARD)
        
        self.patient = URIRef(INDIVO_RECORD_URI%record.id)
        g.add((self.patient, RDF.type, SP['MedicalRecord']))

    ########################
    ### Public Interface ###
    ########################

    def toRDF(self,format="xml"):
        return self.g.serialize(format=format)

    def addDemographics(self, record):
        """ Adds patient Demographics info to the graph. """

        # TODO: Implement with Indivo demographics model
        pNode = BNode()
        self.addStatement(pNode)
        g.add((pNode,RDF.type,SP.Demographics))
       
        nameNode = BNode()
        g.add((pNode, VCARD['n'], nameNode))
        g.add((nameNode,RDF.type, VCARD['Name']))
        g.add((nameNode,VCARD['given-name'],Literal(p.fname)))
        g.add((nameNode,VCARD['additional-name'],Literal(p.initial)))
        g.add((nameNode,VCARD['family-name'],Literal(p.lname)))
        
        addrNode = BNode() 
        g.add((pNode, VCARD['adr'], addrNode))
        g.add((addrNode, RDF.type, VCARD['Address']))
        g.add((addrNode, RDF.type, VCARD['Home']))
        g.add((addrNode, RDF.type, VCARD['Pref']))
        g.add((addrNode,VCARD['street-address'],Literal(p.street)))
        if len(p.apartment) > 0: g.add((addrNode,VCARD['extended-address'],Literal(p.apartment)))
        g.add((addrNode,VCARD['locality'],Literal(p.city)))
        g.add((addrNode,VCARD['region'],Literal(p.region)))
        g.add((addrNode,VCARD['postal-code'],Literal(p.pcode)))
        g.add((addrNode,VCARD['country'],Literal(p.country)))
      
        if len(p.home) > 0:
            homePhoneNode = BNode() 
            g.add((pNode, VCARD['tel'], homePhoneNode))
            g.add((homePhoneNode, RDF.type, VCARD['Tel']))
            g.add((homePhoneNode, RDF.type, VCARD['Home']))
            g.add((homePhoneNode, RDF.type, VCARD['Pref']))
            g.add((homePhoneNode,RDF.value,Literal(p.home)))
           
        if len(p.cell) > 0:
            cellPhoneNode = BNode() 
            g.add((pNode, VCARD['tel'], cellPhoneNode))
            g.add((cellPhoneNode, RDF.type, VCARD['Tel']))
            g.add((cellPhoneNode, RDF.type, VCARD['Cell']))
            if len(p.home) == 0: g.add((cellPhoneNode, RDF.type, VCARD['Pref']))
            g.add((cellPhoneNode,RDF.value,Literal(p.cell)))
      
        g.add((pNode,FOAF['gender'],Literal(p.gender)))
        g.add((pNode,VCARD['bday'],Literal(p.dob)))
        g.add((pNode,VCARD['email'],Literal(p.email)))

        recordNode = BNode()
        g.add((pNode,SP['medicalRecordNumber'],recordNode))
        g.add((recordNode, RDF.type, SP['Code']))
        g.add((recordNode, DCTERMS['title'], Literal("My Hospital Record %s"%p.pid)))
        g.add((recordNode, DCTERMS['identifier'], Literal(p.pid)))
        g.add((recordNode, SP['system'], Literal("My Hospital Record")))
        
    def addMedList(self, meds):
        """Adds a MedList to a patient's graph"""

        g = self.g
        if not meds: return # no meds

        for m in meds:
            mNode = self.medication(m)
            self.addStatement(mNode)

            # Now,loop through and add fulfillments for each med
            for fill in m.fulfillments.all().iterator():
                self.addFill(fill, medNode=mNode)

    def addFill(self, fill, medNode=None, med_uri_only=True):
        """ Build a Fill and add it to the patient graph, optionally linking it with a medication node. """
        g = self.g
        rfNode = URIRef(fill.uri('fullfillments'))
        g.add((rfNode, RDF.type, SP['Fulfillment']))
        g.add((rfNode, DCTERMS['date'], Literal(fill.date)))
        g.add((rfNode, SP['dispenseDaysSupply'], Literal(fill.dispenseDaysSupply)))
        if fill.pbm:
            g.add((rfNode, SP['pbm'], Literal(fill.pbm)))

        pharmNode = self.pharmacy(fill, 'pharmacy')
        if pharmNode:
            g.add((rfNode, SP['pharmacy'], pharmNode))

        provNode = self.provider(fill, 'provider')
        if provNode:
            g.add((rfNode, SP['provider'], provNode))

        if fill.quantityDispensed_value and fill.quantityDispensed_unit:
            g.add((rfNode, SP['quantityDispensed'], self.valueAndUnit(fill.quantityDispensed_value,
                                                                      fill.quantityDispensed_unit)))

        if medNode: # link from medication to us
            g.add((medNode, SP['fulfillment'], rfNode))

        # link from us to medication, just a URI or a whole Node if required
        if fill.medication and med_uri_only: 
            g.add((rfNode, SP['medication'], URIRef(fill.medication.uri())))
        elif fill.medication and not med_uri_only:
            g.add((rfNode, SP['medication'], medNode))

        self.addStatement(rfNode)
    
    def addFillList(self, fills):
        """ Adds a FillList to a patient's graph. """
        g = self.g
        if not fills: return # no fills

        addedMeds = {}
        for f in fills:

            # get the med node, creating it if we need to
            medNode = addedMeds.get(f.medication.id, None)
            if not medNode:
                medNode = self.medication(f.medication)
                self.addStatement(medNode)
                addedMeds[f.medication.id] = medNode

            self.addFill(f, medNode=medNode, med_uri_only=False)

    def addProblemList(self, problems):
        """Add problems to a patient's graph"""
        g = self.g

        for prob in problems:
            pnode = URIRef(prob.uri())
            g.add((pnode, RDF.type, SP['Problem']))
            g.add((pnode, SP['startDate'], Literal(prob.startDate)))      
            if prob.endDate:
                g.add((pnode, SP['endDate'], Literal(prob.endDate)))
            if prob.notes:
                g.add((pnode, SP['notes'], Literal(prob.notes)))
            g.add((pnode, SP['problemName'],
                   self.codedValue(SPCODE["SNOMED"],
                                   SNOMED_URI%prob.name_identifier,
                                   prob.name_title,
                                   SNOMED_URI%"",
                                   prob.name_identifier)))
            self.addStatement(pnode)
            
    def addEncounterList(self, encounters):
        """Add encounters to a patient's graph"""
        g = self.g

        for encounter in encounters:
            eNode = URIRef(encounter.uri())
            g.add((eNode, RDF.type, SP['Encounter']))
            g.add((eNode, SP['startDate'], Literal(encounter.startDate)))      
            if encounter.endDate:
                g.add((eNode, SP['endDate'], Literal(encounter.endDate)))
                
            orgNode = self.organization(encounter, 'facility')
            if orgNode:
                g.add((eNode, SP['organization'], orgNode))

            provNode = self.provider(encounter, 'provider')
            if provNode:
                g.add((eNode, SP['provider'], provNode))
                
            g.add((eNode, SP['encounterType'],
                   self.codedValue(SPCODE["EncounterType"],
                                   ENC_TYPE_URI%encounter.encounterType_identifier,
                                   encounter.encounterType_title,
                                   ENC_TYPE_URI%"",
                                   encounter.encounterType_identifier)))
            self.addStatement(eNode)

    def addVitalSigns(self):
        """Add vitals to a patient's graph"""

        # TODO: adapt to Indivo Vitals
        g = self.g
        if not self.pid in VitalSigns.vitals: return # No vitals to add

        for v in VitalSigns.vitals[self.pid]:
            vnode = BNode()
            self.addStatement(vnode)
            g.add((vnode,RDF.type,SP['VitalSigns']))
            g.add((vnode,dcterms.date, Literal(v.timestamp)))

            enode = BNode()
            g.add((enode,RDF.type,SP['Encounter']))
            g.add((vnode,SP.encounter, enode))
            g.add((enode,SP.startDate, Literal(v.start_date)))
            g.add((enode,SP.endDate, Literal(v.end_date)))

            if v.encounter_type == 'ambulatory':
                etype = ontology_service.coded_value(g, URIRef("http://smartplatforms.org/terms/codes/EncounterType#ambulatory"))
                g.add((enode, SP.encounterType, etype))
        
            def attachVital(vt, p):
                ivnode = BNode()
                if hasattr(v, vt['name']):
                    val = getattr(v, vt['name'])
                    g.add((ivnode, sp.value, Literal(val)))
                    g.add((ivnode, RDF.type, sp.VitalSign))
                    g.add((ivnode, sp.unit, Literal(vt['unit'])))
                    g.add((ivnode, sp.vitalName, ontology_service.coded_value(g, URIRef(vt['uri']))))
                    g.add((p, sp[vt['predicate']], ivnode))
                return ivnode

            for vt in VitalSigns.vitalTypes:
                attachVital(vt, vnode)

            if v.systolic:
                bpnode = BNode()
                g.add((vnode, sp.bloodPressure, bpnode))
                attachVital(VitalSigns.systolic, bpnode)
                attachVital(VitalSigns.diastolic, bpnode)
            
            self.addStatement(vnode)

    def addImmunizationList(self, immunizations):
        """Add immunizations to a patient's graph"""
        g = self.g

        for i in immunizations:

            inode = URIRef(i.uri())
            g.add((inode, RDF.type, SP['Immunization']))

            g.add((inode, DCTERMS['date'], Literal(i.date)))
            g.add((inode, SP['administrationStatus'],
                   self.codedValue(
                        SPCODE["ImmunizationAdministrationStatus"],
                        IMM_STATUS_URI%i.administration_status_identifier,
                        i.administration_status_title,
                        IMM_STATUS_URI%"",
                        i.administration_status_identifier)))
            g.add((inode, SP['productName'],
                   self.codedValue(
                        SP['ImmunizationProduct'],
                        IMM_PROD_URI%i.product_name_identifier,
                        i.product_name_title,
                        IMM_PROD_URI%"",
                        i.product_name_identifier)))
        
            if i.product_class_title and i.product_class_identifier:
                g.add((inode, SP['productClass'],
                       self.codedValue(
                            SP['ImmunizationClass'],
                            IMM_CLASS_URI%i.product_class_identifier,
                            i.product_class_title,
                            IMM_CLASS_URI%"",
                            i.product_class_identifier)))
                                
            if i.product_class_2_title and i.product_class_2_identifier:
                g.add((inode, SP['productClass'],
                       self.codedValue(
                            SP['ImmunizationClass'],
                            IMM_CLASS_URI%i.product_class_2_identifier,
                            i.product_class_2_title,
                            IMM_CLASS_URI%"",
                            i.product_class_2_identifier)))
            
            if i.refusal_reason_title and i.refusal_reason_identifier:
                g.add((inode, SP['refusalReason'], 
                       self.codedValue(
                            SP['ImmunizationRefusalReason'],
                            IMM_REFUSE_URI%i.refusal_reason_identifier,
                            i.refusal_reason_title,
                            IMM_REFUSE_URI%"",
                            i.refusal_reason_identifier)))
                            
            self.addStatement(inode)

    def addLabResults(self):
        """Adds Lab Results to the patient's graph"""
       
        # TODO: Adapt to Indivo LabResults

        g = self.g
        if not self.pid in Lab.results: return  #No labs
        for lab in Lab.results[self.pid]:
            lNode = BNode()
            g.add((lNode,RDF.type,SP['LabResult']))
            g.add((lNode,SP['labName'],
                   self.codedValue(SPCODE["LOINC"], LOINC_URI%lab.code,lab.name,LOINC_URI%"",lab.code)))

            if lab.scale=='Qn':
                qNode = BNode()
                g.add((qNode,RDF.type,SP['QuantitativeResult']))
                g.add((qNode,SP['valueAndUnit'],
                       self.valueAndUnit(lab.value,lab.units)))

                # Add Range Values
                rNode = BNode()
                g.add((rNode,RDF.type,SP['ValueRange']))
                g.add((rNode,SP['minimum'],
                       self.valueAndUnit(lab.low,lab.units)))
                g.add((rNode,SP['maximum'],
                       self.valueAndUnit(lab.high,lab.units)))
                g.add((qNode,SP['normalRange'],rNode)) 
                g.add((lNode,SP['quantitativeResult'],qNode))

            if lab.scale=='Ord': # Handle an Ordinal Result  
                qNode = BNode()
                g.add((qNode,RDF.type,SP['NarrativeResult']))
                g.add((qNode,SP['value'],Literal(lab.value)))
                g.add((lNode,SP['narrativeResult'],qNode))

            aNode = BNode()
            g.add((aNode,RDF.type,SP['Attribution']))
            g.add((aNode,SP['startDate'],Literal(lab.date)))
            g.add((lNode,SP['specimenCollected'],aNode))

            g.add((lNode,SP['externalID'],Literal(lab.acc_num)))      
            self.addStatement(lNode)

    def addAllergyExclusions(self, exclusions):
        """ Add allergy exclusions to the patient graph. """
        g = self.g

        for e in exclusions:
            aExcept = URIRef(e.uri('allergy_exclusions'))
            g.add((aExcept, RDF.type, SP['AllergyExclusion']))
            g.add((aExcept, SP['allergyExclusionName'],
                   self.codedValue(
                        SPCODE["AllergyExclusion"],
                        SNOMED_URI%e.name_identifier,
                        e.name_title,
                        SNOMED_URI%'',
                        e.name_identifier)))
            self.addStatement(aExcept)

    def addAllergyList(self, allergies):
        """ Add a list of allergies to the patient graph. """
        g = self.g

        for a in allergies:            
            aNode = URIRef(a.uri('allergies'))
            g.add((aNode, RDF.type, SP['Allergy']))
            g.add((aNode, SP['severity'],
                   self.codedValue(
                        SPCODE["AllergySeverity"],
                        SNOMED_URI%a.severity_identifier, 
                        a.severity_title,
                        SNOMED_URI%'',
                        a.severity_identifier)))
            g.add((aNode, SP['allergicReaction'],
            self.codedValue(
                       SPCODE["SNOMED"],
                       SNOMED_URI%a.allergic_reaction_identifier,
                       a.allergic_reaction_title,
                       SNOMED_URI%'',
                       a.allergic_reaction_identifier)))
            g.add((aNode, SP['category'],
                   self.codedValue(
                        SPCODE["AllergyCategory"],
                        SNOMED_URI%a.category_identifier,
                        a.category_title, 
                        SNOMED_URI%'',
                        a.category_identifier)))

            if a.drug_allergen_identifier and a.drug_allergen_title:
                g.add((aNode, SP['drugAllergen'],
                       self.codedValue(
                            SPCODE["RxNorm_Ingredient"],
                            RXN_URI%a.drug_allergen_identifier,
                            a.drug_allergen_title,
                            RXN_URI%'',
                            a.drug_allergen_identifier)))

            elif a.drug_class_allergen_identifier and a.drug_class_allergen_title:
                g.add((aNode, SP['drugClassAllergen'],
                       self.codedValue(
                            SPCODE["NDFRT"],
                            NUI_URI%a.drug_class_allergen_identifier,
                            a.drug_class_allergen_title,
                            NUI_URI%'',
                            a.drug_class_allergen_identifier)))

            elif a.food_allergen_identifier and a.food_allergen_title:
                g.add((aNode, SP['foodAllergen'],
                       self.codedValue(
                            SPCODE["UNII"],
                            UNII_URI%a.food_allergen_identifier,
                            a.food_allergen_title,
                            UNII_URI%'',
                            a.food_allergen_identifier)))
            self.addStatement(aNode)

    #####################################################
    ### Helper Methods for reusable low-level objects ###
    #####################################################

    def medication(self, m):
        """ Build a Medication, but don't add fills and don't link it to the patient. Returns the med node. """
        g = self.g
        if not m: return # no med

        mNode = URIRef(m.uri())
        g.add((mNode, RDF.type, SP['Medication']))
        g.add((mNode, SP['drugName'], 
               self.codedValue(
                    SPCODE["RxNorm_Semantic"], 
                    RXN_URI%m.drugName_identifier,
                    m.drugName_title,
                    RXN_URI%"",
                    m.drugName_identifier)))
        g.add((mNode, SP['startDate'], Literal(m.startDate)))
        g.add((mNode, SP['instructions'], Literal(m.instructions))) 
        if m.quantity_value and m.quantity_unit:
            g.add((mNode, SP['quantity'], self.valueAndUnit(m.quantity_value, m.quantity_unit)))
        if m.frequency_value and m.frequency_unit:
            g.add((mNode, SP['frequency'], self.valueAndUnit(m.frequency_value, m.frequency_unit)))
        if m.endDate:
            g.add((mNode, SP['endDate'], Literal(m.endDate)))
        if m.provenance_identifier and m.provenance_title and m.provenance_system:
            g.add((mNode, SP['provenance'],
                   self.codedValue(
                        SPCODE['MedicationProvenance'],
                        MED_PROV_URI%m.provenance_identifier,
                        m.provenance_title,
                        MED_PROV_URI%"",
                        m.provenance_identifier)))
        return mNode

    def codedValue(self,codeclass,uri,title,system,identifier):
        """ Adds a CodedValue to the graph and returns node"""
        if not (codeclass or uri or title or system or identifier): return None

        cvNode=BNode()
        self.g.add((cvNode, RDF.type, SP['CodedValue']))
        self.g.add((cvNode, DCTERMS['title'], Literal(title)))
        
        cNode=URIRef(uri)
        self.g.add((cvNode, SP['code'], cNode))

        # Two types:  the general "Code" and specific, e.g. "BloodPressureCode"
        self.g.add((cNode, RDF.type, codeclass))
        self.g.add((cNode, RDF.type, SP['Code']))

        self.g.add((cNode, DCTERMS['title'], Literal(title)))
        self.g.add((cNode, SP['system'], Literal(system)))
        self.g.add((cNode, DCTERMS['identifier'], Literal(identifier)))
        return cvNode

    def valueAndUnit(self,value,units):
        """Adds a ValueAndUnit node to a graph; returns the node"""
        if not value and not units: return None

        vNode = BNode()
        self.g.add((vNode, RDF.type, SP['ValueAndUnit']))
        self.g.add((vNode, SP['value'], Literal(value)))
        self.g.add((vNode, SP['unit'], Literal(units)))
        return vNode

    def address(self, obj, prefix):
        suffixes = ['country', 'city', 'postalcode', 'region', 'street']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        addrNode = BNode() 
        self.g.add((addrNode, RDF.type, VCARD['Address']))

        if fields['street']:
            self.g.add((addrNode, VCARD['street-address'], Literal(fields['street'])))

        if fields['city']:
            self.g.add((addrNode, VCARD['locality'], Literal(fields['city'])))
            
        if fields['region']:
            self.g.add((addrNode, VCARD['region'], Literal(fields['region'])))

        if fields['postalcode']:
            self.g.add((addrNode, VCARD['postal-code'], Literal(fields['postalcode'])))

        if fields['country']:
            self.g.add((addrNode, VCARD['country'], Literal(fields['country'])))

        return addrNode

    def telephone(self, obj, prefix):
        suffixes = ['type', 'number', 'preferred_p']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        tNode = BNode()
        self.g.add((tNode, RDF.type, VCARD['Tel']))
        
        if fields['type']:
            self.g.add((tNode, RDF.type, VCARD[getattr(obj, 'get_%s_type_display'%(prefix))()]))
        if fields['preferred_p'] and fields['preferred_p']:
            self.g.add((tNode, RDF.type, VCARD['Pref']))
        if fields['number']:
            self.g.add((tNode, RDF['value'], Literal(fields['number'])))

        return tNode

    def name(self, obj, prefix):
        suffixes = ['family', 'given', 'prefix', 'suffix']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        nNode = BNode()
        self.g.add((nNode, RDF.type, VCARD['Name']))

        if fields['family']:
            self.g.add((nNode, VCARD['family-name'], Literal(fields['family'])))
        if fields['given']:
            self.g.add((nNode, VCARD['given-name'], Literal(fields['given'])))
        if fields['prefix']:
            self.g.add((nNode, VCARD['honorific-prefix'], Literal(fields['prefix'])))
        if fields['suffix']:
            self.g.add((nNode, VCARD['honorific-suffix'], Literal(fields['suffix'])))

        return nNode

    def organization(self, obj, prefix):
        suffixes = ['name', 'adr_country', 'adr_city', 'adr_postalcode', 'adr_region', 'adr_street']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        oNode = BNode()
        self.g.add((oNode, RDF.type, SP['Organization']))

        if fields['name']:
            self.g.add((oNode, VCARD['organization-name'], Literal(fields['name'])))
        addrNode = self.address(obj, "%s_adr"%prefix)
        if addrNode:
            self.g.add((oNode, VCARD['adr'], addrNode))
        return oNode

    def pharmacy(self, obj, prefix):
        suffixes = ['ncpdpid', 'org', 'adr_country', 'adr_city', 'adr_postalcode', 'adr_region', 'adr_street']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        pNode = BNode()
        self.g.add((pNode, RDF.type, SP['Pharmacy']))

        if fields['ncpdpid']:
            self.g.add((pNode, SP['ncpdpId'], Literal(fields['ncpdpid'])))
        if fields['org']:
            self.g.add((pNode, VCARD['organization-name'], Literal(fields['org'])))
        addrNode = self.address(obj, "%s_adr"%prefix)
        if addrNode:
            self.g.add((pNode, VCARD['adr'], addrNode))
        return pNode

    def provider(self, obj, prefix):
        suffixes = ['dea_number', 'ethnicity', 'npi_number', 'preferred_language', 'race', 'bday', 'email', 'gender']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        pNode = BNode()
        self.g.add((pNode, RDF.type, SP['Provider']))

        self.g.add((pNode, VCARD['n'], self.name(obj, "%s_name"%prefix))) # name is required
        if fields['dea_number']:
            self.g.add((pNode, SP['deaNumber'], Literal(fields['dea_number'])))
        if fields['ethnicity']:
            self.g.add((pNode, SP['ethnicity'], Literal(fields['ethnicity'])))
        if fields['npi_number']:
            self.g.add((pNode, SP['npiNumber'], Literal(fields['npi_number'])))
        if fields['preferred_language']:
            self.g.add((pNode, SP['preferredLanguage'], Literal(fields['preferred_language'])))
        if fields['race']:
            self.g.add((pNode, SP['race'], Literal(fields['race'])))
        if fields['bday']:
            self.g.add((pNode, VCARD['bday'], Literal(fields['bday'])))
        if fields['email']:
            self.g.add((pNode, VCARD['email'], Literal(fields['email'])))
        if fields['gender']:
            self.g.add((pNode, FOAF['gender'], Literal(fields['gender'])))

        addrNode = self.address(obj, "%s_adr"%prefix)
        if addrNode:
            self.g.add((pNode, VCARD['adr'], addrNode))

        tel1Node = self.telephone(obj, "%s_tel_1"%prefix)
        if tel1Node:
            self.g.add((pNode, VCARD['tel'], tel1Node))

        tel2Node = self.telephone(obj, "%s_tel_2"%prefix)
        if tel2Node:
            self.g.add((pNode, VCARD['tel'], tel2Node))

        return pNode

    ################################
    ### Low-level helper methods ###
    ################################

    def _obj_fields_by_name(self, obj, prefix, suffixes):
        """ Given an object, returns a dictionary of its attributes based on prefix and suffixes.
        
        Specifically, the dictionary is of the form::
        
          {
            'suffix': getattr(obj, prefix + '_' + suffix)
          }
          
        for each suffix in suffixes.
        
        """

        ret = dict([(s, getattr(obj, "%s_%s"%(prefix, s))) for s in suffixes])
        if not reduce(lambda x, y: x or y, ret.values()): # return None if we found none of our fields
            return None
        return ret

    def addStatement(self, s):
        self.g.add((s, SP['belongsTo'], self.patient))

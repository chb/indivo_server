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
        
        self.patient = BNode()
        g.add((self.patient, RDF.type, SP['MedicalRecord']))

    def codedValue(self,codeclass,uri,title,system,identifier):
        """ Adds a CodedValue to the graph and returns node"""
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
        vNode = BNode()
        self.g.add((vNode, RDF.type, SP['ValueAndUnit']))
        self.g.add((vNode, SP['value'], Literal(value)))
        self.g.add((vNode, SP['unit'], Literal(units)))
        return vNode

    def toRDF(self,format="xml"):
        return self.g.serialize(format=format)

    def addStatement(self, s):
        #      self.g.add((self.patient, SP['hasStatement'], s))
        self.g.add((s, SP['belongsTo'], self.patient))

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

        # TODO: adopt to Indivo Meds Model

        g = self.g
        if not meds: return # no meds

        for m in meds:
            mNode = BNode()
            g.add((mNode, RDF.type, SP['Medication']))
            g.add((mNode, SP['drugName'], self.codedValue(SPCODE["RxNorm_Semantic"], RXN_URI%m.rxn,m.name,RXN_URI%"",m.rxn)))
            g.add((mNode,SP['startDate'],Literal(m.start)))
            g.add((mNode,SP['instructions'],Literal(m.sig))) 
            if m.qtt:
                g.add((mNode,SP['quantity'],self.valueAndUnit(m.qtt,m.qttunit)))
            if m.freq:
                g.add((mNode,SP['frequency'],self.valueAndUnit(m.freq,m.frequnit)))

            self.addStatement(mNode)

            # Now,loop through and add fulfillments for each med
            for fill in Refill.refill_list(m.pid,m.rxn):
                rfNode = BNode()
                g.add((rfNode,RDF.type,SP['Fulfillment']))
                g.add((rfNode,DCTERMS['date'],Literal(fill.date)))
                g.add((rfNode,SP['dispenseQuantity'], self.valueAndUnit(fill.q,"{tab}")))
                
                g.add((rfNode,SP['dispenseDaysSupply'],Literal(fill.days)))
                
                g.add((rfNode,SP['medication'],mNode)) # create bidirectional links
                g.add((mNode,SP['fulfillment'],rfNode))
                self.addStatement(rfNode)

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

    def addImmunizations(self):
        """Add immunizations to a patient's graph"""

        # TODO: Adapt to Indivo Immunizations
       
        g = self.g

        if not self.pid in Immunizations.immunizations: return # No immunizations to add

        for i in Immunizations.immunizations[self.pid]:

            inode = BNode()
            self.addStatement(inode)
            g.add((inode,RDF.type,SP['Immunization']))
            g.add((inode,dcterms.date, Literal(v.timestamp)))
            g.add((inode, sp.administrationStatus, ontology_service.coded_value(g, URIRef(i.administration_status))))
            
            if i.refusal_reason:
                g.add((inode, sp.refusalReason, ontology_service.coded_value(g, URIRef(i.refusal_reason))))

            cvx_system, cvx_id = i.cvx.rsplit("#",1)
            g.add((inode, sp.productName, self.codedValue(SPCODE["ImmunizationProduct"],URIRef(i.cvx), i.cvx_title, cvx_system+"#", cvx_id)))

            if (i.vg):
                vg_system, vg_id = i.vg.rsplit("#",1)
                g.add((inode, sp.productClass, self.codedValue(SPCODE["ImmunizationClass"],URIRef(i.vg), i.vg_title, vg_system+"#", vg_id)))

            if (i.vg2):
                vg2_system, vg2_id = i.vg2.rsplit("#",1)
                g.add((inode, sp.productClass, self.codedValue(SPCODE["ImmunizationClass"],URIRef(i.vg2), i.vg2_title, vg2_system+"#", vg2_id)))

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

    def addAllergies(self):
        """A totally bogus method: doesn't read from an allergy file!"""
        # TODO: adapt for Indivo Allergies
        g = self.g

        if int(self.pid)%100 < 85:  # no allergies for ~ 85% of population
            aExcept = BNode()
            g.add((aExcept,RDF.type,SP['AllergyExclusion']))
            g.add((aExcept,SP['allergyExclusionName'],
                   self.codedValue(SPCODE["AllergyExclusion"],SNOMED_URI%'160244002','no known allergies',SNOMED_URI%'','160244002')))
            self.addStatement(aExcept)
        else:  # Sprinkle in some sulfa allergies, for pid ending 85 and up
            aNode = BNode()
            g.add((aNode,RDF.type,SP['Allergy']))
            g.add((aNode,SP['severity'],
                   self.codedValue(SPCODE["AllergySeverity"],SNOMED_URI%'255604002','mild',SNOMED_URI%'','255604002')))
            g.add((aNode,SP['allergicReaction'],
                   self.codedValue(SPCODE["SNOMED"],SNOMED_URI%'271807003','skin rash',SNOMED_URI%'','271807003')))
            g.add((aNode,SP['category'],
                   self.codedValue(SPCODE["AllergyCategory"],SNOMED_URI%'416098002','drug allergy', SNOMED_URI%'','416098002')))
            g.add((aNode,SP['drugClassAllergen'],
                   self.codedValue(SPCODE["NDFRT"],NUI_URI%'N0000175503','sulfonamide antibacterial',NUI_URI%''.split('&')[0], 'N0000175503')))
            self.addStatement(aNode)
            if int(self.pid)%2: # And throw in some peanut allergies if odd pid...
                aNode = BNode()
                g.add((aNode,RDF.type,SP['Allergy'])) 
                g.add((aNode,SP['severity'],
                       self.codedValue(SPCODE["AllergySeverity"],SNOMED_URI%'24484000','severe',SNOMED_URI%'','24484000')))
                g.add((aNode,SP['allergicReaction'],
                       self.codedValue(SPCODE["SNOMED"],SNOMED_URI%'39579001','anaphylaxis',SNOMED_URI%'','39579001')))
                g.add((aNode,SP['category'],
                       self.codedValue(SPCODE["AllergyCategory"],SNOMED_URI%'414285001','food allergy',SNOMED_URI%'','414285001')))
                g.add((aNode,SP['foodAllergen'],
                       self.codedValue(SPCODE["UNII"],UNII_URI%'QE1QX6B99R','peanut',UNII_URI%'','QE1QX6B99R')))
                self.addStatement(aNode)
                

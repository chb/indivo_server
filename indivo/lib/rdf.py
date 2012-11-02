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
LAB_INTERP_URI="http://smartplatforms.org/terms/codes/LabResultInterpretation#%s"
LAB_STATUS_URI="http://smartplatforms.org/terms/codes/LabStatus#%s"

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
        
    ########################
    ### Public Interface ###
    ########################

    def toRDF(self,format="xml"):
        return self.g.serialize(format=format)
    
    def addDemographics(self, record):
        """ Adds patient Demographics info to the graph. """
        g = self.g
        demographics = record.demographics

        dNode = URIRef(demographics.uri())
        g.add((dNode, RDF.type, SP['Demographics']))
        
        # simple required
        g.add((dNode, VCARD['bday'], Literal(demographics.bday)))
        g.add((dNode, FOAF['gender'], Literal(demographics.gender)))    
        
        # simple optional
        if demographics.ethnicity:
            g.add((dNode, SP['ethnicity'], Literal(demographics.ethnicity)))
        if demographics.preferred_language:
            g.add((dNode, SP['preferredLanguage'], Literal(demographics.preferred_language)))
        if demographics.race:
            g.add((dNode, SP['race'], Literal(demographics.race)))
        if demographics.email:
            g.add((dNode, SP['email'], Literal(demographics.email)))
       
        # compound required
        self.g.add((dNode, VCARD['n'], self.name(demographics, "name")))
        g.add((dNode, SP['medicalRecordNumber'],
               self.code("Indivo Record %s"%record.id,
                         "Indivo Record",
                         INDIVO_RECORD_URI%record.id,
                         blank=True)))
        
        # compound optional           
        addrNode = self.address(demographics, "adr")
        if addrNode:
            self.g.add((dNode, VCARD['adr'], addrNode))
        tel1Node = self.telephone(demographics, "tel_1")
        if tel1Node:
            self.g.add((dNode, VCARD['tel'], tel1Node))
        tel2Node = self.telephone(demographics, "tel_2")
        if tel2Node:
            self.g.add((dNode, VCARD['tel'], tel2Node))

        self.addStatement(dNode)

    def addMedList(self, meds):
        """Adds a MedList to a patient's graph"""

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
                
            problem_name = self._getCodedValueFromField(prob, 'name', [SPCODE['SNOMED']])    
            g.add((pnode, SP['problemName'], self.newCodedValue(problem_name)))
            self.addStatement(pnode)
            
    def addEncounterList(self, encounters):
        """Add encounters to a patient's graph"""
        g = self.g

        for encounter in encounters:
            eNode = self.encounter(encounter)
            self.addStatement(eNode)

    def addVitalsList(self, vitals):
        """Add vitals to a patient's graph"""
        g = self.g

        for v in vitals:
            vnode = URIRef(v.uri('vital_signs'))
            g.add((vnode, RDF.type, SP['VitalSignSet']))
            g.add((vnode, DCTERMS['date'], Literal(v.date)))

            enode = self.encounter(v.encounter)
            self.addStatement(enode)
            g.add((vnode, SP['encounter'], enode))

            bpNode = self.bloodPressure(v, 'bp')
            if bpNode:
                g.add((vnode, SP['bloodPressure'], bpNode))

            bmiNode = self.vital(v, 'bmi')
            if bmiNode:
                g.add((vnode, SP['bodyMassIndex'], bmiNode))

            hrNode = self.vital(v, 'heart_rate')
            if hrNode:
                g.add((vnode, SP['heartRate'], hrNode))

            hNode = self.vital(v, 'height')
            if hNode:
                g.add((vnode, SP['height'], hNode))

            osNode = self.vital(v, 'oxygen_saturation')
            if osNode:
                g.add((vnode, SP['oxygenSaturation'], osNode))
                
            rrNode = self.vital(v, 'respiratory_rate')
            if rrNode:
                g.add((vnode, SP['respiratoryRate'], rrNode))
                
            tNode = self.vital(v, 'temperature')
            if tNode:
                g.add((vnode, SP['temperature'], tNode))

            wNode = self.vital(v, 'weight')
            if wNode:
                g.add((vnode, SP['weight'], wNode))
                
            hcNode = self.vital(v, 'head_circ')
            if hcNode:
                g.add((hcNode, SP['headCircumference'], hcNode))
        
            self.addStatement(vnode)

    def addImmunizationList(self, immunizations):
        """Add immunizations to a patient's graph"""
        g = self.g

        for i in immunizations:

            inode = URIRef(i.uri())
            g.add((inode, RDF.type, SP['Immunization']))

            g.add((inode, DCTERMS['date'], Literal(i.date)))
            
            admin_status = self._getCodedValueFromField(i, 'administration_status', [SPCODE['ImmunizationAdministrationStatus']])
            g.add((inode, SP['administrationStatus'], self.newCodedValue(admin_status)))
            
            product_name = self._getCodedValueFromField(i, 'product_name', [SPCODE['ImmunizationProduct']])
            g.add((inode, SP['productName'], self.newCodedValue(product_name)))
        
            product_class = self._getCodedValueFromField(i, 'product_class', [SPCODE['ImmunizationClass']])
            if i.product_class_title and i.product_class_identifier:
                g.add((inode, SP['productClass'], self.newCodedValue(product_class)))
                                
            product_class2 = self._getCodedValueFromField(i, 'product_class_2', [SPCODE['ImmunizationClass']])
            if i.product_class_2_title and i.product_class_2_identifier:
                g.add((inode, SP['productClass'], self.newCodedValue(product_class2)))
            
            refusal_reason = self._getCodedValueFromField(i, 'refusal_reason', [SPCODE['ImmunizationRefusalReason']])
            if i.refusal_reason_title and i.refusal_reason_identifier:
                g.add((inode, SP['refusalReason'], self.newCodedValue(refusal_reason)))
                            
            self.addStatement(inode)

    def addLabList(self, labs):
        """Adds Lab Results to the patient's graph"""
        g = self.g

        for lab in labs:
            lNode = URIRef(lab.uri('lab_results'))
            g.add((lNode, RDF.type, SP['LabResult']))

            lab_name = self._getCodedValueFromField(lab, 'name', [SPCODE['LOINC']])
            g.add((lNode , SP['labName'], self.newCodedValue(lab_name)))
            
            if lab.abnormal_interpretation_title and lab.abnormal_interpretation_identifier:
                abnormal_interpretation = self._getCodedValueFromField(lab, 'abnormal_interpretation', [SPCODE['LabResultInterpretation']])
                g.add((lNode, SP['abnormalInterpretation'], self.newCodedValue(abnormal_interpretation)))

            if lab.accession_number:
                g.add((lNode, SP['accessionNumber'], Literal(lab.accession_number)))

            if lab.status_title and lab.status_identifier:
                lab_status = self._getCodedValueFromField(lab, 'status', [SPCODE['LabResultStatus']])
                g.add((lNode, SP['labStatus'], self.newCodedValue(lab_status)))

            if lab.narrative_result:
                nrNode = BNode()
                g.add((nrNode, RDF.type, SP['NarrativeResult']))
                g.add((nrNode, SP['value'], Literal(lab.narrative_result)))
                g.add((lNode, SP['narrativeResult'], nrNode))

            if lab.notes:
                g.add((lNode, SP['notes'], Literal(lab.notes)))

            qrNode = self.quantitativeResult(lab, 'quantitative_result')
            if qrNode:
                g.add((lNode, SP['quantitativeResult'], qrNode))

            
            self.addStatement(lNode)

    def addAllergyExclusions(self, exclusions):
        """ Add allergy exclusions to the patient graph. """
        g = self.g

        for e in exclusions:
            aExcept = URIRef(e.uri('allergy_exclusions'))
            g.add((aExcept, RDF.type, SP['AllergyExclusion']))
            exclusion_name = self._getCodedValueFromField(e, 'name', [SPCODE["AllergyExclusion"]])
            g.add((aExcept, SP['allergyExclusionName'], self.newCodedValue(exclusion_name)))
            self.addStatement(aExcept)

    def addAllergyList(self, allergies):
        """ Add a list of allergies to the patient graph. """
        g = self.g

        for a in allergies:            
            aNode = URIRef(a.uri('allergies'))
            g.add((aNode, RDF.type, SP['Allergy']))
            
            severity = self._getCodedValueFromField(a, 'severity', [SPCODE["AllergySeverity"]])
            g.add((aNode, SP['severity'], self.newCodedValue(severity)))
            
            reaction = self._getCodedValueFromField(a, 'allergic_reaction', [SPCODE["SNOMED"]])
            g.add((aNode, SP['allergicReaction'], self.newCodedValue(reaction)))
            
            category = self._getCodedValueFromField(a, 'category', [SPCODE["AllergyCategory"]])
            g.add((aNode, SP['category'], self.newCodedValue(category)))

            if a.drug_allergen_code_identifier and a.drug_allergen_code_title:
                drug_allergen = self._getCodedValueFromField(a, 'drug_allergen', [SPCODE["RxNorm_Ingredient"]])
                g.add((aNode, SP['drugAllergen'], self.newCodedValue(drug_allergen)))

            elif a.drug_class_allergen_code_identifier and a.drug_class_allergen_code_title:
                drug_class_allergen = self._getCodedValueFromField(a, 'drug_class_allergen', [SPCODE["NDFRT"]])
                g.add((aNode, SP['drugClassAllergen'], self.newCodedValue(drug_class_allergen)))

            elif a.other_allergen_code_identifier and a.other_allergen_code_title:
                other_allergen = self._getCodedValueFromField(a, 'other_allergen', [SPCODE["UNII"]])
                g.add((aNode, SP['otherAllergen'], self.newCodedValue(other_allergen)))
            self.addStatement(aNode)

    def addProcedureList(self, procedures):
        """Add procedures to a patient's graph"""
        g = self.g

        for procedure in procedures:
            pnode = URIRef(procedure.uri())
            g.add((pnode, RDF.type, SP['Procedure']))
            
            # required
            procedure_name = self._getCodedValueFromField(procedure, 'name', [SPCODE['SNOMED']])
            g.add((pnode, SP['procedureName'], self.newCodedValue(procedure_name)))
            
            # optional
            if procedure.date:
                g.add((pnode, SP['date'], Literal(procedure.date)))      
            if procedure.notes:
                g.add((pnode, SP['notes'], Literal(procedure.notes)))
                
            procedure_status = self._getCodedValueFromField(procedure, 'status', [SPCODE['SNOMED']])
            if procedure_status:    
                g.add((pnode, SP['procedureStatus'], self.newCodedValue(procedure_status)))
            
            procedure_provider = self.provider(procedure, 'provider')
            if procedure_provider:
                g.add((pnode, SP['provider'], procedure_provider))
            
            self.addStatement(pnode)

    def addSocialHistoryList(self, histories):
        """Add social histories to a patient's graph"""
        
        g = self.g

        for history in histories:
            hnode = URIRef(history.uri())
            g.add((hnode, RDF.type, SP['SocialHistory']))
            
            # optional
            smoking_status = self._getCodedValueFromField(history, 'smoking_status', [SPCODE['SmokingStatus']])
            if smoking_status:    
                g.add((hnode, SP['smokingStatus'], self.newCodedValue(smoking_status)))
            
            self.addStatement(hnode)
            
    def addClinicalNoteList(self, notes):
        """Add clinical notes to a patient's graph"""
        
        g = self.g

        for note in notes:
            nnode = URIRef(note.uri())
            g.add((nnode, RDF.type, SP['ClinicalNote']))
            
            # required
            document_with_format = BNode();
            g.add((document_with_format, RDF.type, SP['DocumentWithFormat']))
            g.add((document_with_format, DCTERMS['format'], Literal(note.format)))
            if note.value:
                g.add((document_with_format, DCTERMS['value'], Literal(note.value)))

            g.add((nnode, DCTERMS['hasFormat'], document_with_format))

            # optional
            if note.date:
                g.add((nnode, DCTERMS['date'], Literal(note.date)))
            if note.title:
                g.add((nnode, DCTERMS['title'], Literal(note.title))) 
                
            note_provider = self.provider(note, 'provider')
            if note_provider:
                g.add((nnode, SP['provider'], note_provider))
            
            self.addStatement(nnode)

    #####################################################
    ### Helper Methods for reusable low-level objects ###
    #####################################################

    def encounter(self, encounter):
        """Build an Encounter, but don't link it to a patient graph"""
        g = self.g

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
                
        encounter_type = self._getCodedValueFromField(encounter, 'type', SPCODE["EncounterType"])
        g.add((eNode, SP['encounterType'], self.newCodedValue(encounter_type)))
        return eNode

    def medication(self, m):
        """ Build a Medication, but don't add fills and don't link it to the patient. Returns the med node. """
        g = self.g
        if not m: return # no med

        mNode = URIRef(m.uri())
        g.add((mNode, RDF.type, SP['Medication']))
        
        drug_name = self._getCodedValueFromField(m, 'name', SPCODE["RxNorm_Semantic"])
        g.add((mNode, SP['drugName'], self.newCodedValue(drug_name)))
        g.add((mNode, SP['startDate'], Literal(m.startDate)))
        g.add((mNode, SP['instructions'], Literal(m.instructions or ''))) 
        if m.quantity_value and m.quantity_unit:
            g.add((mNode, SP['quantity'], self.valueAndUnit(m.quantity_value, m.quantity_unit)))
        if m.frequency_value and m.frequency_unit:
            g.add((mNode, SP['frequency'], self.valueAndUnit(m.frequency_value, m.frequency_unit)))
        if m.endDate:
            g.add((mNode, SP['endDate'], Literal(m.endDate)))
        if m.provenance_identifier and m.provenance_title and m.provenance_system:
            provenance = self._getCodeFromField(m, 'provenance', [SPCODE['MedicationProvenance']])
            g.add((mNode, SP['provenance'],
                   self.new_code(provenance)))
        return mNode

    def newCodedValue(self, coded_value):
        """ Adds a CodedValue to the graph and returns a node"""
        
        if not coded_value:
            return None
        
        title = coded_value.get('title', '')
        code = coded_value.get('code', None)
        provenance = coded_value.get('provenance', None)
        
        cv_node = BNode()
        
        self.g.add((cv_node, RDF.type, SP['CodedValue']))
        self.g.add((cv_node, DCTERMS['title'], Literal(title)))

        # sp:code
        code_node = self.new_code(code)
        if code_node:
            self.g.add((cv_node, SP['code'], code_node))
            
        # sp:provenance
        provenance_node = self.codeProvenance(provenance)
        if provenance_node:
            self.g.add((cv_node, SP['provenance'], provenance_node))
        
        return cv_node
        

    def new_code(self, code, blank=False):
        """ Adds a Code to the graph and returns node """
        
        if not code or (code.get("identifier") is None and code.get("title") is None and code.get("system") is None):
            # don't add Codes that are empty
            return None
        
        classes = code.get("classes", [])
        title = code.get("title", "")
        system = code.get("system", "")
        identifier = code.get("identifier", "")
        
        if blank:
            node = BNode()
        else:
            node = URIRef(system + identifier)
        self.g.add((node, RDF.type, SP['Code']))
        self.g.add((node, DCTERMS['title'], Literal(title)))
        self.g.add((node, SP['system'], Literal(system)))
        self.g.add((node, DCTERMS['identifier'], Literal(identifier)))

        # Add additional types: the general "Code" and specific, e.g. "BloodPressureCode"        
        for c in classes:
            self.g.add((node, RDF.type, c))
        return node

    def code(self, title, system, identifier, blank=False, classes=[]):
        """ Adds a Code to the graph and returns node """
        if blank:
            node = BNode()
        else:
            node = URIRef(system+identifier)
        self.g.add((node, RDF.type, SP['Code']))
        self.g.add((node, DCTERMS['title'], Literal(title)))
        self.g.add((node, SP['system'], Literal(system)))
        self.g.add((node, DCTERMS['identifier'], Literal(identifier)))

        # Add additional types: the general "Code" and specific, e.g. "BloodPressureCode"        
        for c in classes:
            self.g.add((node, RDF.type, c))
        return node

    def codeProvenance(self, provenance):
        """ Adds a CodeProvenance to the graph and returns node """
        
        title = provenance.get("title", None)
        source_code = provenance.get("sourceCode", None)
        translation_fidelity = provenance.get("translationFidelity", None)
        
        node = BNode()
        self.g.add((node, DCTERMS['title'], Literal(title)))
        self.g.add((node, DCTERMS['sourceCode'], Literal(source_code)))
        
        translation_fidelity_node = self.new_code(translation_fidelity)
        if translation_fidelity_node:
            self.g.add((node, SPCODE['TranslationFidelity'], translation_fidelity_node))
        

    def codedValue(self,codeclass,uri,title,system,identifier):
        """ Adds a CodedValue to the graph and returns node"""
        if not (codeclass or uri or title or system or identifier): return None

        cvNode=BNode()
        self.g.add((cvNode, RDF.type, SP['CodedValue']))
        self.g.add((cvNode, DCTERMS['title'], Literal(title)))

        cNode=self.code(title, system, identifier, classes=[codeclass])
        self.g.add((cvNode, SP['code'], cNode))

        return cvNode

    def codedValueFromObj(self, obj, prefix, codeclass):
        suffixes = ['identifier', 'title', 'system']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        return self.codedValue(
            codeclass,
            fields['system'] + fields['identifier'],
            fields['title'],
            fields['system'],
            fields['identifier'],
            )

    def valueAndUnit(self,value,units):
        """Adds a ValueAndUnit node to a graph; returns the node"""
        if not value and not units: return None

        vNode = BNode()
        self.g.add((vNode, RDF.type, SP['ValueAndUnit']))
        self.g.add((vNode, SP['value'], Literal(value)))
        self.g.add((vNode, SP['unit'], Literal(units)))
        return vNode

    def valueAndUnitFromObj(self, obj, prefix):
        val = getattr(obj, '%s_value'%prefix, None)
        unit = getattr(obj, '%s_unit'%prefix, None)
        return self.valueAndUnit(val, unit)

    def valueRange(self, obj, prefix):
        """Adds a ValueRange node to a graph; returns the node"""
        vrNode = BNode()

        minNode = self.valueAndUnitFromObj(obj, "%s_min"%prefix)
        if minNode:
            self.g.add((vrNode, SP['minimum'], minNode))

        maxNode = self.valueAndUnitFromObj(obj, "%s_max"%prefix)
        if maxNode:
            self.g.add((vrNode, SP['maximum'], minNode))
            
        if not minNode and not maxNode:
            return None

        self.g.add((vrNode, RDF.type, SP['ValueRange']))
        return vrNode

    def quantitativeResult(self, obj, prefix):
        """Adds a QuantitativeResult node to a graph; returns the node"""
        qrNode = BNode()

        ncrNode = self.valueRange(obj, '%s_non_critical_range'%prefix)
        if ncrNode:
            self.g.add((qrNode, SP['nonCriticalRange'], ncrNode))

        nrNode = self.valueRange(obj, '%s_normal_range'%prefix)
        if nrNode:
            self.g.add((qrNode, SP['normalRange'], nrNode))

        vuNode = self.valueAndUnitFromObj(obj, '%s_value'%prefix)
        if vuNode:
            self.g.add((qrNode, SP['valueAndUnit'], vuNode))

        if vuNode:
            self.g.add((qrNode, RDF.type, SP['QuantitativeResult']))
            return qrNode
        return None

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
        if not fields or not fields['number']:
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
        suffixes = ['family', 'given', 'middle', 'prefix', 'suffix']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        nNode = BNode()
        self.g.add((nNode, RDF.type, VCARD['Name']))

        if fields['family']:
            self.g.add((nNode, VCARD['family-name'], Literal(fields['family'])))
        if fields['given']:
            self.g.add((nNode, VCARD['given-name'], Literal(fields['given'])))
        if fields['middle']:
            self.g.add((nNode, VCARD['additional-name'], Literal(fields['middle'])))
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

    def vital(self, obj, prefix):
        suffixes = ['unit', 'value']
        fields = self._obj_fields_by_name(obj, prefix, suffixes)
        if not fields:
            return None

        vNode = BNode()
        self.g.add((vNode, RDF.type, SP['VitalSign']))

        if fields['unit']:
            self.g.add((vNode, SP['unit'], Literal(fields['unit'])))
        if fields['value']:
            self.g.add((vNode, SP['value'], Literal(fields['value'])))

        nameNode = self.codedValueFromObj(obj, "%s_name"%prefix, SPCODE['VitalSign'])
        if nameNode:
            self.g.add((vNode, SP['vitalName'], nameNode))

        return vNode

    def bloodPressure(self, obj, prefix):
        bpNode = BNode()
        self.g.add((bpNode, RDF.type, SP['BloodPressure']))
        
        sysNode = self.vital(obj, "%s_systolic"%prefix)
        if sysNode:
            self.g.add((bpNode, SP['systolic'], sysNode))

        diaNode = self.vital(obj, "%s_diastolic"%prefix)
        if diaNode:
            self.g.add((bpNode, SP['diastolic'], diaNode))

        posNode = self.codedValueFromObj(obj, "%s_position"%prefix, SPCODE['BloodPressureBodyPosition'])
        if posNode:
            self.g.add((bpNode, SP['bodyPosition'], posNode))

        siteNode = self.codedValueFromObj(obj, "%s_site"%prefix, SPCODE['BloodPressureBodySite'])
        if siteNode:
            self.g.add((bpNode, SP['bodySite'], siteNode))

        methodNode = self.codedValueFromObj(obj, "%s_method"%prefix, SPCODE['BloodPressureMethod'])
        if methodNode:
            self.g.add((bpNode, SP['method'], methodNode))

        return bpNode
    
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
        self.g.add((s, SP['belongsTo'], URIRef(INDIVO_RECORD_URI%self.record.id)))


    def _getCodedValueFromField(self, model, field_prefix, classes=None):
        """ Build up a dictionary representing a sp:CodedValue """
        
        coded_value = {}
        
        try:
            coded_value["title"] = getattr(model, '%s_title' % (field_prefix))
            coded_value["code"] = self._getCodeFromField(model, "%s_code" % (field_prefix), classes)
            coded_value["provenance"] = self._getProvenanceFromField(model, "%s_provenance" % (field_prefix))
        except AttributeError:
            raise #TODO
        
        return coded_value

    def _getCodeFromField(self, model, field_prefix, classes=None):
        """ Build up a dictionary representing a sp:code """
        
        classes = classes or []
        code = {}
        
        try:
            code["classes"] = classes
            code["identifier"] = getattr(model, '%s_identifier' % (field_prefix))
            code["title"] = getattr(model, '%s_title' % (field_prefix))
            code["system"] = getattr(model, '%s_system' % (field_prefix))
        except AttributeError:
            raise #TODO
        
        return code
            
    def _getProvenanceFromField(self, model, field_prefix):
        """ Build up a dictionary representing a sp:provenance """
        
        provenance = {}
        
        try:
            provenance["title"] = getattr(model, '%s_title' % (field_prefix))
            provenance["sourceCode"] = getattr(model, '%s_source_code' % (field_prefix))
            translation_fidelity = self._getCodeFromField(model, "%s_translation_fidelity" % (field_prefix), classes=[SPCODE['TranslationFidelity']])
            provenance["translationFidelity"] = translation_fidelity
        except AttributeError:
            raise #TODO
        
        return provenance

    
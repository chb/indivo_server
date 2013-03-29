SMART_MEDICATION_RDF_XML = [
    """<?xml version="1.0" encoding="utf-8"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sp="http://smartplatforms.org/terms#"
                 xmlns:spcode="http://smartplatforms.org/terms/codes/" xmlns:dcterms="http://purl.org/dc/terms/">
            <sp:Medication>
                <sp:drugName>
                    <sp:CodedValue>
                        <dcterms:title>PREVACID 30 MG CAPSULE</dcterms:title>
                        <sp:code>
                            <spcode:RxNorm_Semantic rdf:about="http://purl.bioontology.org/ontology/RXNORM/206206">
                                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
                                <sp:system>http://purl.bioontology.org/ontology/RXNORM/</sp:system>
                                <dcterms:identifier>206206</dcterms:identifier>
                                <dcterms:title>Prevacid 30 MG Enteric Coated Capsule</dcterms:title>
                            </spcode:RxNorm_Semantic>
                        </sp:code>
                        <sp:provenance>
                            <sp:CodeProvenance>
                                <sp:sourceCode rdf:resource="http://fda.gov/NDC/00300304613"/>
                                <dcterms:title>PREVACID 30 MG CAPSULE</dcterms:title>
                                <sp:translationFidelity>
                                    <spcode:TranslationFidelity rdf:about="http://smartplatforms.org/terms/codes/TranslationFidelity#automated">
                                        <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" />
                                        <dcterms:title>Automated</dcterms:title>
                                        <sp:system>http://smartplatforms.org/terms/codes/TranslationFidelity#</sp:system>
                                        <dcterms:identifier>automated</dcterms:identifier>
                                    </spcode:TranslationFidelity>
                                </sp:translationFidelity>
                            </sp:CodeProvenance>
                        </sp:provenance>
                    </sp:CodedValue>
                </sp:drugName>
                <sp:startDate>2013-02-18</sp:startDate>
                <sp:endDate>2013-09-18</sp:endDate>
                <sp:instructions>TAKE 1 TABLET TWICE DAILY WITH MEALS</sp:instructions>
                <sp:quantity>
                    <sp:ValueAndUnit>
                        <sp:value>2</sp:value>
                        <sp:unit>{tablet}</sp:unit>
                    </sp:ValueAndUnit>
                </sp:quantity>
                <sp:frequency>
                    <sp:ValueAndUnit>
                        <sp:value>2</sp:value>
                        <sp:unit>/d</sp:unit>
                    </sp:ValueAndUnit>
                </sp:frequency>
                <sp:provenance>
                    <sp:Code>
                        <dcterms:title>ProvenanceTitle</dcterms:title>
                        <dcterms:identifier>1234</dcterms:identifier>
                        <sp:system>ProvenanceSystem</sp:system>
                    </sp:Code>
                </sp:provenance>
            </sp:Medication>
        </rdf:RDF>
    """,
    """<?xml version="1.0" encoding="utf-8"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sp="http://smartplatforms.org/terms#"
                 xmlns:v="http://www.w3.org/2006/vcard/ns#"
                 xmlns:spcode="http://smartplatforms.org/terms/codes/" xmlns:dcterms="http://purl.org/dc/terms/">
            <sp:Medication>
                <sp:drugName>
                    <sp:CodedValue>
                        <dcterms:title>PREVACID 30 MG CAPSULE</dcterms:title>
                        <sp:code>
                            <spcode:RxNorm_Semantic rdf:about="http://purl.bioontology.org/ontology/RXNORM/206206">
                                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
                                <sp:system>http://purl.bioontology.org/ontology/RXNORM/</sp:system>
                                <dcterms:identifier>206206</dcterms:identifier>
                                <dcterms:title>Prevacid 30 MG Enteric Coated Capsule</dcterms:title>
                            </spcode:RxNorm_Semantic>
                        </sp:code>
                        <sp:provenance>
                            <sp:CodeProvenance>
                                <sp:sourceCode rdf:resource="http://fda.gov/NDC/00300304613"/>
                                <dcterms:title>PREVACID 30 MG CAPSULE</dcterms:title>
                                <sp:translationFidelity
                                        rdf:resource="http://smartplatforms.org/terms/codes/TranslationFidelity#automated"/>
                            </sp:CodeProvenance>
                        </sp:provenance>
                    </sp:CodedValue>
                </sp:drugName>
                <sp:startDate>2013-02-18</sp:startDate>
                <sp:instructions>TAKE 1 TABLET TWICE DAILY WITH MEALS</sp:instructions>
                <sp:quantity>
                    <sp:ValueAndUnit>
                        <sp:value>2</sp:value>
                        <sp:unit>{tablet}</sp:unit>
                    </sp:ValueAndUnit>
                </sp:quantity>
                <sp:frequency>
                    <sp:ValueAndUnit>
                        <sp:value>2</sp:value>
                        <sp:unit>/d</sp:unit>
                    </sp:ValueAndUnit>
                </sp:frequency>
                <sp:fulfillment>
                    <sp:Fulfillment rdf:about="http://sandbox-api.smartplatforms.org/records/2169591/fulfillments/63221">
                        <sp:belongsTo rdf:resource="http://sandbox-api.smartplatforms.org/records/2169591" />
                        <dcterms:date>2010-05-12T04:00:00Z</dcterms:date>
                        <sp:medication rdf:resource="http://sandbox-api.smartplatforms.org/records/2169591/medications/123" />
                        <sp:provider>
                            <sp:Provider>
                                <v:n>
                                    <v:Name>
                                        <v:given-name>Joshua</v:given-name>
                                        <v:family-name>Mandel</v:family-name>
                                    </v:Name>
                                </v:n>
                                <sp:npiNumber>5235235</sp:npiNumber>
                                <sp:deaNumber>325555555</sp:deaNumber>
                                <v:email>test@stuff.com</v:email>
                                <v:email>other@stuff.com</v:email>
                            </sp:Provider>
                        </sp:provider>
                        <sp:pharmacy>
                            <sp:Pharmacy>
                                <sp:ncpdpId>5235235</sp:ncpdpId>
                                <v:organization-name>CVS #588</v:organization-name>
                                <v:adr>
                                    <v:Address>
                                        <v:street-address>111 Lake Drive</v:street-address>
                                        <v:locality>WonderCity</v:locality>
                                        <v:postal-code>5555</v:postal-code>
                                        <v:country-name>Australia</v:country-name>
                                    </v:Address>
                                </v:adr>
                            </sp:Pharmacy>
                        </sp:pharmacy>
                        <sp:pbm>T00000000001011</sp:pbm>
                        <sp:quantityDispensed>
                            <sp:ValueAndUnit>
                                <sp:value>60</sp:value>
                                <sp:unit>{tablet}</sp:unit>
                            </sp:ValueAndUnit>
                        </sp:quantityDispensed>
                        <sp:dispenseDaysSupply>30</sp:dispenseDaysSupply>
                    </sp:Fulfillment>
                </sp:fulfillment>
            </sp:Medication>
        </rdf:RDF>
    """,
]


SMART_FULFILLMENT_RDF_XML = [
    """<?xml version="1.0" encoding="utf-8"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:sp="http://smartplatforms.org/terms#"
                xmlns:spcode="http://smartplatforms.org/terms/codes/"
                xmlns:dcterms="http://purl.org/dc/terms/"
                xmlns:v="http://www.w3.org/2006/vcard/ns#"
                xmlns:foaf="http://xmlns.com/foaf/0.1/">
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
                                <v:additional-name>test_additinal_name</v:additional-name>
                                <v:honorific-prefix>test_prefix</v:honorific-prefix>
                                <v:honorific-suffix>test_suffix</v:honorific-suffix>
                            </v:Name>
                        </v:n>
                        <sp:npiNumber>5235235</sp:npiNumber>
                        <sp:deaNumber>325555555</sp:deaNumber>
                        <v:email>test@stuff.com</v:email>
                        <v:email>other@stuff.com</v:email>
                        <sp:ethnicity>test_ethnicity</sp:ethnicity>
                        <sp:preferredLanguage>test_preferred_language</sp:preferredLanguage>
                        <sp:race>test_race</sp:race>
                        <v:adr>
                            <v:Address>
                                <v:region>test_region</v:region>
                                <v:extended-address>test_extended_address</v:extended-address>
                                <v:street-address>test_address</v:street-address>
                                <v:locality>test_locality</v:locality>
                                <v:postal-code>test_postal</v:postal-code>
                                <v:country-name>test_country</v:country-name>
                            </v:Address>
                        </v:adr>
                        <v:bday>01/01/1945</v:bday>
                        <v:tel>
                            <v:Tel>
                                <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Home" />
                                <rdf:value>555-5555</rdf:value>
                            </v:Tel>
                        </v:tel>
                        <v:tel>
                            <v:Tel>
                                <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Work" />
                                <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Pref" />
                                <rdf:value>800-555-1212</rdf:value>
                            </v:Tel>
                        </v:tel>
                        <foaf:gender>male</foaf:gender>
                    </sp:Provider>
                </sp:provider>
                <sp:pharmacy>
                    <sp:Pharmacy>
                        <sp:ncpdpId>5235235</sp:ncpdpId>
                        <v:organization-name>CVS #588</v:organization-name>
                        <v:adr>
                            <v:Address>
                                <v:region>test_region</v:region>
                                <v:extended-address>test_extended_address</v:extended-address>
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
        </rdf:RDF>
    """,
    # duplicate info for the same subject
    """<?xml version="1.0" encoding="utf-8"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sp="http://smartplatforms.org/terms#"
                 xmlns:spcode="http://smartplatforms.org/terms/codes/" xmlns:dcterms="http://purl.org/dc/terms/"
                 xmlns:v="http://www.w3.org/2006/vcard/ns#">
            <sp:Fulfillment rdf:about="http://sandbox-api.smartplatforms.org/records/2169591/fulfillments/63221">
                <sp:belongsTo rdf:resource="http://sandbox-api.smartplatforms.org/records/2169591" />
                <dcterms:date>2010-06-12T04:00:00Z</dcterms:date>
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
        </rdf:RDF>
    """,
    ]


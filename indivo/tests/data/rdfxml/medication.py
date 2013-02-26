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
            </sp:Medication>
        </rdf:RDF>
    """,
    ]
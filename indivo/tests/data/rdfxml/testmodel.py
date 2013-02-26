TEST_MODEL_RDF_XML = [
    """<?xml version="1.0" encoding="utf-8"?>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sp="http://smartplatforms.org/terms#"
             xmlns:spcode="http://smartplatforms.org/terms/codes/" xmlns:dcterms="http://purl.org/dc/terms/">
        <sp:TestModel>
            <sp:name>
                <sp:CodedValue>
                    <dcterms:title>Test Title 1</dcterms:title>
                    <sp:code>
                        <spcode:Code rdf:about="http://test.org/ontology/TEST/1">
                            <rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
                            <sp:system>http://test.org/ontology/TEST/</sp:system>
                            <dcterms:identifier>1</dcterms:identifier>
                            <dcterms:title>Test Title 2</dcterms:title>
                        </spcode:Code>
                    </sp:code>
                    <sp:provenance>
                        <sp:CodeProvenance>
                            <sp:sourceCode rdf:resource="http://provenance.test.org/ontology/TEST/1"/>
                            <dcterms:title>Test Title 3</dcterms:title>
                            <sp:translationFidelity
                                    rdf:resource="http://smartplatforms.org/terms/codes/TranslationFidelity#automated"/>
                        </sp:CodeProvenance>
                    </sp:provenance>
                </sp:CodedValue>
            </sp:name>
            <sp:simpleDateElement>2013-02-18</sp:simpleDateElement>
            <sp:simpleStringElement>TEST STRING 1</sp:simpleStringElement>
            <sp:simpleIntegerElement>1</sp:simpleIntegerElement>
            <sp:quantity>
                <sp:ValueAndUnit>
                    <sp:value>1</sp:value>
                    <sp:unit>{tablet}</sp:unit>
                </sp:ValueAndUnit>
            </sp:quantity>
        </sp:TestModel>
        <sp:TestModel>
            <sp:name>
                <sp:CodedValue>
                    <dcterms:title>Test Title 4</dcterms:title>
                    <sp:code>
                        <spcode:Code rdf:about="http://test.org/ontology/TEST/2">
                            <rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
                            <sp:system>http://test.org/ontology/TEST/</sp:system>
                            <dcterms:identifier>2</dcterms:identifier>
                            <dcterms:title>Test Title 5</dcterms:title>
                        </spcode:Code>
                    </sp:code>
                    <sp:provenance>
                        <sp:CodeProvenance>
                            <sp:sourceCode rdf:resource="http://provenance.test.org/ontology/TEST/2"/>
                            <dcterms:title>Test Title 6</dcterms:title>
                            <sp:translationFidelity
                                    rdf:resource="http://smartplatforms.org/terms/codes/TranslationFidelity#automated"/>
                        </sp:CodeProvenance>
                    </sp:provenance>
                </sp:CodedValue>
            </sp:name>
            <sp:simpleDateElement>2010-03-18</sp:simpleDateElement>
            <sp:simpleStringElement>TEST STRING 2</sp:simpleStringElement>
            <sp:simpleIntegerElement>2</sp:simpleIntegerElement>
            <sp:quantity>
                <sp:ValueAndUnit>
                    <sp:value>2</sp:value>
                    <sp:unit>{tablet}</sp:unit>
                </sp:ValueAndUnit>
            </sp:quantity>
        </sp:TestModel>
        <sp:TestModel>
            <sp:simpleDateElement>2011-03-18</sp:simpleDateElement>
            <sp:simpleStringElement>TEST STRING 3</sp:simpleStringElement>
            <sp:simpleIntegerElement>3</sp:simpleIntegerElement>
            <sp:optionalSimpleStringElement>optional</sp:optionalSimpleStringElement>
        </sp:TestModel>
    </rdf:RDF>
    """,
]
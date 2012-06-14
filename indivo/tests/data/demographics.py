from indivo.models import Demographics
from base import ForeignKey, TestModel, scope

class TestDemographics(TestModel):
    # small subset of actual demographics info
    model_fields = ['name_family', 'name_given', 'bday', 'gender', 'email', 'document']
    model_class = Demographics

    def _setupargs(self, family_name, given_name, bday, gender, email=None, demographics_doc=None):
        self.name_family = family_name
        self.name_given = given_name
        self.bday = bday
        self.gender = gender
        self.email = email
        self.document = demographics_doc

_TEST_DEMOGRAPHICS = [
    {'family_name':'Wayne',
     'given_name': 'Bruce',
     'email': 'test@fake.org',
     'bday': '1939-11-15',
     'gender': 'male',
     'demographics_doc': ForeignKey('document', 'TEST_DEMOGRAPHICS_DOCS', 0)
     },
    {'family_name':'Testerson',
     'given_name': 'Test',
     'email': 'test2@fake.org',
     'bday': '1975-01-19',
     'gender': 'female',
     'demographics_doc': ForeignKey('document', 'TEST_DEMOGRAPHICS_DOCS', 1)
     },
    {'family_name':'McGee',
     'given_name': 'Testy',
     'email': 'test3@fake.org',
     'bday': '1985-06-01',
     'gender': 'female',
     'demographics_doc': ForeignKey('document', 'TEST_DEMOGRAPHICS_DOCS', 2)
     },
]
TEST_DEMOGRAPHICS = scope(_TEST_DEMOGRAPHICS, TestDemographics)


TEST_DEMOGRAPHICS_XML = '''
    <Demographics xmlns="http://indivo.org/vocab/xml/documents#">
        <dateOfBirth>1939-11-15</dateOfBirth>
        <gender>male</gender>
        <email>test@fake.org</email>
        <ethnicity>Scottish</ethnicity>
        <preferredLanguage>EN</preferredLanguage>
        <race>caucasian</race>
        <Name>
            <familyName>Wayne</familyName>
            <givenName>Bruce</givenName>
            <prefix>Mr</prefix>
            <suffix>Jr</suffix>
        </Name>
        <Telephone>
            <type>h</type>
            <number>555-5555</number>
            <preferred>true</preferred>
        </Telephone>
        <Telephone>
            <type>c</type>
            <number>555-6666</number>
            <preferred>false</preferred>
        </Telephone>
        <Address>
            <country>USA</country>
            <city>Gotham</city>
            <postalCode>90210</postalCode>
            <region>secret</region>
            <street>1007 Mountain Drive</street>
        </Address>
    </Demographics>
'''

TEST_DEMOGRAPHICS_RDFXML = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/"    
             xmlns:foaf="http://xmlns.com/foaf/0.1/"    
             xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"    
             xmlns:sp="http://smartplatforms.org/terms#"    
             xmlns:v="http://www.w3.org/2006/vcard/ns#" >
        <rdf:Description rdf:about="http://indivo.org/records/65c9e500-fdcf-4ba3-87ed-6eb265344d84/demographics">
            <v:n rdf:nodeID="_d9d1cbfe-46b9-4534-80cc-c3558cde379f"/>
            <foaf:gender>male</foaf:gender>
            <sp:belongsTo rdf:resource="http://indivo.org/records/65c9e500-fdcf-4ba3-87ed-6eb265344d84"/>
            <sp:ethnicity>Scottish</sp:ethnicity>
            <sp:preferredLanguage>EN</sp:preferredLanguage>
            <rdf:type rdf:resource="http://smartplatforms.org/terms#Demographics"/>
            <v:adr rdf:nodeID="_32774cc8-7eed-45f2-8a1b-663e6c90553b"/>
            <sp:email>test@fake.org</sp:email>
            <v:tel rdf:nodeID="_1f1e7c5d-69c7-466f-bc6e-3b3866adb055"/>
            <v:tel rdf:nodeID="_ab23417c-7d76-4c87-98d1-f081a84e9a10"/>
            <sp:race>caucasian</sp:race>
            <sp:medicalRecordNumber rdf:resource="Indivo Recordhttp://indivo.org/records/65c9e500-fdcf-4ba3-87ed-6eb265344d84"/>
            <v:bday rdf:datatype="http://www.w3.org/2001/XMLSchema#date">1939-11-15</v:bday>
        </rdf:Description>
        <rdf:Description rdf:nodeID="_d9d1cbfe-46b9-4534-80cc-c3558cde379f">
            <v:given-name>Bruce</v:given-name>
            <v:honorific-prefix>Mr</v:honorific-prefix>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Name"/>
            <v:honorific-suffix>Jr</v:honorific-suffix>
            <v:family-name>Wayne</v:family-name>
        </rdf:Description>
        <rdf:Description rdf:about="Indivo Recordhttp://indivo.org/records/65c9e500-fdcf-4ba3-87ed-6eb265344d84">
            <sp:system>Indivo Record</sp:system>
            <rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
            <dcterms:identifier>http://indivo.org/records/65c9e500-fdcf-4ba3-87ed-6eb265344d84</dcterms:identifier>
            <dcterms:title>Indivo Record 65c9e500-fdcf-4ba3-87ed-6eb265344d84</dcterms:title>
        </rdf:Description>
        <rdf:Description rdf:nodeID="_32774cc8-7eed-45f2-8a1b-663e6c90553b">
            <v:locality>Gotham</v:locality>
            <v:country>USA</v:country>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Address"/>
            <v:region>secret</v:region>
            <v:postal-code>90210</v:postal-code>
            <v:street-address>1007 Mountain Drive</v:street-address>
        </rdf:Description>
        <rdf:Description rdf:nodeID="_ab23417c-7d76-4c87-98d1-f081a84e9a10">
            <rdf:value>555-5555</rdf:value>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Tel"/>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Pref"/>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Home"/>
        </rdf:Description>
        <rdf:Description rdf:nodeID="_1f1e7c5d-69c7-466f-bc6e-3b3866adb055">
            <rdf:value>555-6666</rdf:value>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Cell"/>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Tel"/>
            <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Pref"/>
        </rdf:Description>
    </rdf:RDF>
'''

TEST_DEMOGRAPHICS_SDMX = '''
    <Models>
        <Model name="Demographics">
            <Field name="bday">1939-11-15T00:00:00Z</Field>
            <Field name="email">test@fake.org</Field>
            <Field name="ethnicity">Scottish</Field>
            <Field name="gender">male</Field>
            <Field name="preferred_language">EN</Field>
            <Field name="race">caucasian</Field>
            <Field name="name_given">Bruce</Field>
            <Field name="name_suffix">Jr</Field>
            <Field name="name_family">Wayne</Field>
            <Field name="name_prefix">Mr</Field>
            <Field name="tel_2_type">c</Field>
            <Field name="tel_2_preferred_p"/>
            <Field name="tel_2_number">555-6666</Field>
            <Field name="adr_region">secret</Field>
            <Field name="adr_country">USA</Field>
            <Field name="adr_postalcode">90210</Field>
            <Field name="adr_city">Gotham</Field>
            <Field name="adr_street">1007 Mountain Drive</Field>
            <Field name="tel_1_type">h</Field>
            <Field name="tel_1_preferred_p">true</Field>
            <Field name="tel_1_number">555-5555</Field>
        </Model>
    </Models>
'''

TEST_DEMOGRAPHICS_SDMJ = '''
    [
        {
            "tel_1_preferred_p": "true",
            "adr_region": "secret",
            "tel_2_number": "555-6666",
            "__modelname__": "Demographics",
            "adr_city": "Gotham",
            "ethnicity": "Scottish",
            "adr_postalcode": "90210",
            "name_family": "Wayne",
            "tel_1_type": "h",
            "tel_2_type": "c",
            "name_prefix": "Mr",
            "email": "test@fake.org",
            "name_given": "Bruce",
            "adr_street": "1007 Mountain Drive",
            "bday": "1939-11-15T00:00:00Z",
            "tel_1_number": "555-5555",
            "preferred_language": "EN",
            "gender": "male",
            "name_suffix": "Jr",
            "tel_2_preferred_p": "false",
            "race": "caucasian",
            "adr_country": "USA"
        }
    ]
'''
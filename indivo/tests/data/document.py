from indivo.models import Document
from base import ForeignKey, TestModel, raw_data_to_objs
import hashlib

class TestDocument(TestModel):
    model_fields = ['content', 'record', 'pha', 'label', 'creator', 'external_id', 'size', 'digest']
    model_class = Document

    def __init__(self, content, record=None, pha_spec=False, 
                 pha=None, label='testing', creator=None, external_id=None):
        self.content = content
        self.record = record
        self.pha = pha
        self.local_external_id = external_id
        if self.pha:
            self.external_id = Document.prepare_external_id(external_id, self.pha, pha_spec, record)
        else:
            self.external_id = None

        if not pha_spec:
            self.pha = None

        self.label = label
        self.creator = creator
        self.size = len(self.content)

        md = hashlib.sha256()
        md.update(self.content)
        self.digest = md.hexdigest()

    def save(self):
        """ Special case: original_id might be a pointer to self, which Key doesn't support. """
        super(TestDocument, self).save()
        if not Document.objects.filter(pk=self.django_obj.original_id).exists():
            self.django_obj.original = None
            self.django_obj.save()

# Docs 1-5 have external ids, docs 6-11 don't
_TEST_R_DOCS = [
    {'label':'rdoc1',
     'content':"<Document id='HELLOWORLD00' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'external_id':'external_rdoc1',
     'pha_spec':False
     },
    {'label':'rdoc2',
     'content':"<Document id='HELLOWORLD01' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'external_id':'external_rdoc2',
     'pha_spec':False
     },
    {'label':'rdoc3',
     'content':"<Document id='HELLOWORLD02' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'external_id':'external_rdoc3',
     'pha_spec':False
     },    
    {'label':'rdoc4',
     'content':"<Document id='HELLOWORLD03' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'external_id':'external_rdoc4',
     'pha_spec':False
     },
    {'label':'rdoc5',
     'content':"<Document id='HELLOWORLD04' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'external_id':'external_rdoc5',
     'pha_spec':False
     },
    {'label':'rdoc6',
     'content':"<Document id='HELLOWORLD05' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
      },
    {'label':'rdoc7',
     'content':"<Document id='HELLOWORLD06' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
 
     },
    {'label':'rdoc8',
     'content':"<Document id='HELLOWORLD07' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     },
    {'label':'rdoc9',
     'content':"<Document id='HELLOWORLD08' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     },
    {'label':'rdoc10',
     'content':"<Document id='HELLOWORLD09' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     },
    {'label':'rdoc11',
     'content':"<Document id='HELLOWORLD10' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     },
]

# Doc 1 has no ext_id, Doc 2 does
_TEST_RA_DOCS = [
    {'label':'radoc1',
     'content':"<Document id='HELLOWORLD01' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'pha_spec':True
     },
    {'label':'radoc2',
     'content':"<Document id='HELLOWORLD02' xmlns='http://indivo.org/vocab#'></Document>",
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'external_id':'external_rdoc4',
     'pha_spec':True
     },
]

# Doc 1 has no ext_id, Doc 2 does
_TEST_A_DOCS = [
    {'label':'adoc1',
     'content':"<Document id='HELLOWORLD01' xmlns='http://indivo.org/vocab#'></Document>",
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'pha_spec':True
     },
    {'label':'adoc2',
     'content':"<Document id='HELLOWORLD02' xmlns='http://indivo.org/vocab#'></Document>",
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'external_id':'external_rdoc4',
     'pha_spec':True
     },
]

_TEST_DEMOGRAPHICS = [
    {'label':'demo1',
     'content':'<Demographics xmlns="http://indivo.org/vocab/xml/documents#"> <foo>bar</foo></Demographics>',
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     },
]

_TEST_CONTACTS = [
    {'label':'cont1',
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'content': '''<Contact id="5326" xmlns="http://indivo.org/vocab/xml/documents#"> 
                     <name> 
                       <fullName>Sebastian Rockwell Cotour</fullName> 
                       <givenName>Sebastian</givenName> 
                       <familyName>Cotour</familyName> 
                     </name> 
                     <email type="personal"> 
                       <emailAddress>scotour@hotmail.com</emailAddress> 
                     </email> 
                     <email type="work"> 
                       <emailAddress>sebastian.cotour@childrens.harvard.edu</emailAddress> 
                     </email> 
                     <address type="home"> 
                       <streetAddress>15 Waterhill Ct.</streetAddress> 
                       <postalCode>53326</postalCode> 
                       <locality>New Brinswick</locality> 
                       <region>Montana</region> 
                       <country>US</country> 
                       <timeZone>-7GMT</timeZone> 
                     </address> 
                     <location type="home"> 
                       <latitude>47N</latitude> 
                       <longitude>110W</longitude> 
                     </location> 
                     <phoneNumber type="home">5212532532</phoneNumber> 
                     <phoneNumber type="work">6217233734</phoneNumber> 
                     <instantMessengerName protocol="aim">scotour</instantMessengerName> 
                   </Contact>'''
     },
    {'label':'cont2',
     'creator':ForeignKey('account', 'TEST_ACCOUNTS',0),
     'record':ForeignKey('record', 'TEST_RECORDS', 0),
     'content': '''<Contact id="5326" xmlns="http://indivo.org/vocab/xml/documents#"> 
                     <name> 
                       <fullName>Sebastian Rockwell Cotour the Second</fullName> 
                       <givenName>Sebastian</givenName> 
                       <familyName>Cotour</familyName> 
                     </name> 
                     <email type="personal"> 
                       <emailAddress>scotour@hotmail.com</emailAddress> 
                     </email> 
                     <email type="work"> 
                       <emailAddress>sebastian.cotour@childrens.harvard.edu</emailAddress> 
                     </email> 
                     <address type="home"> 
                       <streetAddress>15 Waterhill Ct.</streetAddress> 
                       <postalCode>53326</postalCode> 
                       <locality>New Brinswick</locality> 
                       <region>Montana</region> 
                       <country>US</country> 
                       <timeZone>-7GMT</timeZone> 
                     </address> 
                     <location type="home"> 
                       <latitude>47N</latitude> 
                       <longitude>110W</longitude> 
                     </location> 
                     <phoneNumber type="home">5212532532</phoneNumber> 
                     <phoneNumber type="work">6217233734</phoneNumber> 
                     <instantMessengerName protocol="aim">scotour</instantMessengerName> 
                   </Contact>'''
     },
]

TEST_R_DOCS = raw_data_to_objs(_TEST_R_DOCS, TestDocument)
TEST_RA_DOCS = raw_data_to_objs(_TEST_RA_DOCS, TestDocument)
TEST_A_DOCS = raw_data_to_objs(_TEST_A_DOCS, TestDocument)
TEST_DEMOGRAPHICS = raw_data_to_objs(_TEST_DEMOGRAPHICS, TestDocument)
TEST_CONTACTS = raw_data_to_objs(_TEST_CONTACTS, TestDocument)

# For iterating over special docs
SPECIAL_DOCS = {'contact':TEST_CONTACTS[0].content, 'demographics':TEST_DEMOGRAPHICS[0].content}

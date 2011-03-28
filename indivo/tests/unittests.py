"""
Carenet Unit Tests
"""
import django.test
import unittest
from indivo.models import Account, Record, Document, StatusName, Carenet, CarenetDocument, CarenetPHA, CarenetAccount, CarenetAutoshare, Share

CONTACT = '''<Contact id="5326"> <name> <fullName>Sebastian Rockwell Cotour</fullName> <givenName>Sebastian</givenName> <familyName>Cotour</familyName> </name> <email type="personal"> <emailAddress>scotour@hotmail.com</emailAddress> </email> <email type="work"> <emailAddress>sebastian.cotour@childrens.harvard.edu</emailAddress> </email> <address type="home"> <streetAddress>15 Waterhill Ct.</streetAddress> <postalCode>53326</postalCode> <locality>New Brinswick</locality> <region>Montana</region> <country>US</country> <timeZone>-7GMT</timeZone> </address> <location type="home"> <latitude>47N</latitude> <longitude>110W</longitude> </location> <phoneNumber type="home">5212532532</phoneNumber> <phoneNumber type="work">6217233734</phoneNumber> <instantMessengerName protocol="aim">scotour</instantMessengerName> </Contact>'''
class AccountTestCase(unittest.TestCase):
    def setUp(self):
        self.account = Account.objects.create(email = 'foo@foo.com')

    def tearDown(self):
        self.account.delete()
    
    def test_retired(self):
        self.account.set_state("retired")
        self.assertRaises(Exception, lambda: self.account.set_state("active"))

    def test_password(self):
        self.assertRaises(Exception, lambda: self.account.set_username(username='foobar'))
        self.account.set_username_and_password(username='foobar', password='baz')
        self.account.set_username(username='foobar2')

class RecordTestCase(unittest.TestCase):
    def setUp(self):
        self.account = Account.objects.create(email = 'foo@foo.com')
        self.record = Record.objects.create(owner=self.account, label='Foo Record')

    def tearDown(self):
        self.record.delete()
        self.account.delete()

    def test_send_message(self):
        self.record.send_message("foobar-id", self.account, 'testing message', 'testing message body', body_type='plaintext')
        
class CarenetTestCase(unittest.TestCase):
    def setUp(self):
        self.record = Record.objects.create()
        self.status = StatusName.objects.create(name='active')
        self.contact = Document.objects.create(record = self.record, content= CONTACT, size=len(CONTACT), status = self.status)
        self.record.contact = self.contact
        self.record.save()

        self.record.create_default_carenets()
        self.carenet = self.record.carenet_set.all()[0]

    def test_add_doc(self):
        self.carenet.add_doc(self.record.contact)
        assert(self.carenet.contains_doc(self.record.contact))
        assert(self.carenet.contact)

        self.carenet.remove_doc(self.record.contact)
        assert(not self.carenet.contact)
        assert(not self.carenet.contains_doc(self.record.contact))

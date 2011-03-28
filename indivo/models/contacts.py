"""
Indivo Models for Contacts
"""

from django.db import models
from django.conf import settings

from base import BaseModel

from indivo.lib import utils
from xml.dom.minidom import *

'''
<Contact xmlns="http://indivo.org/vocab/xml/documents#">
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
</Contact>
'''

class Contacts(BaseModel):
    full_name = models.CharField(max_length = 200)
    given_name = models.CharField(max_length = 200)
    family_name = models.CharField(max_length=200)
    
    def to_xml(self):
        return render_template_raw('indivo/contacts', {'contact': self}, type='xml')

    @classmethod
    def from_xml(self, xml_str):
        xml_dom = parseString(xml_str)

        contact = Contacts()
        contact.full_name   = utils.get_element_value(xml_dom, 'fullName')
        contact.given_name  = utils.get_element_value(xml_dom, 'givenName')
        contact.family_name = utils.get_element_value(xml_dom, 'familyName')
        return contact
        
    class Meta:
        abstract = True


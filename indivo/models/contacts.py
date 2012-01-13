"""
Indivo Models for Contacts
"""

from django.db import models
from django.conf import settings

from base import BaseModel

from indivo.lib import utils
from lxml import etree

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

class Contacts(object):
    
    ns = 'http://indivo.org/vocab/xml/documents#'
    
    def __init__(self, data={}):
        for attr, val in data.iteritems():
            try:
                setattr(self, attr, val)
            except Exception:
                pass
    
    def to_xml(self):
        return render_template_raw('contacts', {'contact': self}, type='xml')

    def find_text_anywhere(self, xml_etree, tagname):
        full_tag = './/{%s}%s'%(self.ns, tagname)
        return xml_etree.findtext(full_tag)

    @classmethod
    def from_xml(self, xml_str):
        xml_etree = etree.XML(xml_str)

        contact = Contacts()
        contact.full_name = contact.find_text_anywhere(xml_etree, 'fullName')
        contact.given_name = contact.find_text_anywhere(xml_etree, 'givenName')
        contact.family_name = contact.find_text_anywhere(xml_etree, 'familyName')
        contact.email = contact.find_text_anywhere(xml_etree, 'emailAddress')
        contact.street_address  = contact.find_text_anywhere(xml_etree, 'streetAddress')
        contact.region = contact.find_text_anywhere(xml_etree, 'region')
        contact.postal_code = contact.find_text_anywhere(xml_etree, 'postalCode')
        contact.country = contact.find_text_anywhere(xml_etree, 'country')
        contact.phone_numbers = utils.findalltext(xml_etree, '{%s}phoneNumber'%self.ns)
        return contact
        
    class Meta:
        abstract = True


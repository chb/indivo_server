"""
Indivo Models for Demographics
"""

from django.db import models
from django.conf import settings

from base import BaseModel

from indivo.lib import utils
from xml.dom.minidom import *

class Demographics(BaseModel):
    lastname = models.CharField(max_length = 200)
    firstnames = models.CharField(max_length = 200)
    email = models.CharField(max_length=200)
    address = models.TextField()
    birthdate = models.DateField()
    gender = models.CharField(max_length=1)
    
    def to_xml(self):
        return render_template_raw('demographics', {'demographics': self}, type='xml')

    @classmethod
    def from_xml(self, xml_str):
        xml_dom = parseString(xml_str)

        d = Demographics()
        d.lastname = utils.get_element_value(xml_dom, 'lastname')
        d.firstnames = utils.get_element_value(xml_dom, 'firstnames')
        d.email = utils.get_element_value(xml_dom, 'email')
        d.address = utils.get_element_value(xml_dom, 'address')
        d.birthdate = utils.get_element_value(xml_dom, 'birthdate')
        d.gender = utils.get_element_value(xml_dom, 'gender')

        return d
        
    class Meta:
        abstract = True


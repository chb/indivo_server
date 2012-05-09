from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField

class Allergy(Fact):
    allergic_reaction = CodedValueField()
    category = CodedValueField()
    drug_allergen = CodedValueField()
    drug_class_allergen = CodedValueField()
    food_allergen = CodedValueField()
    severity = CodedValueField()
  

from indivo.models import Fact
from indivo.fields import CodedValueField

class Allergy(Fact):
    allergic_reaction = CodedValueField()
    category = CodedValueField()
    drug_allergen = CodedValueField()
    drug_class_allergen = CodedValueField()
    food_allergen = CodedValueField()
    severity = CodedValueField()

class AllergyExclusion(Fact):
    name = CodedValueField()

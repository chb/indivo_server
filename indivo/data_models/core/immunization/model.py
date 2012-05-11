from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField

class Immunization(Fact):
    date = models.DateTimeField(null=True)
    administration_status = CodedValueField()
    product_class = CodedValueField()
    product_name = CodedValueField()
    refusal_reason = CodedValueField()

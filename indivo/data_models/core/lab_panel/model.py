from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField

class LabPanel(Fact):
    name = CodedValueField()
    
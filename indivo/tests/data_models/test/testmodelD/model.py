from indivo.models import Fact
from django.db import models

class TestModelD(Fact):
    date = models.DateTimeField(null=True)
    text = models.TextField(null=True)
    myA = models.ForeignKey('TestModelA', null=True, related_name='myDs')

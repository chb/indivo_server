from indivo.models import Fact
from django.db import models

class TestModelA(Fact):
    date = models.DateTimeField(null=True)
    text = models.TextField(null=True)
    myBs = models.ManyToManyField('TestModelB', null=True)
    myC = models.OneToOneField('TestModelC', null=True)

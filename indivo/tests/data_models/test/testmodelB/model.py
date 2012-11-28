from indivo.models import Fact
from django.db import models

class TestModelB(Fact):
    date = models.DateTimeField(null=True)
    text = models.TextField(null=True)

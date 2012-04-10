from indivo.models import Fact
from django.db import models

class SimpleClinicalNote(Fact):
    date_of_visit = models.DateTimeField()
    finalized_at = models.DateTimeField(null=True)
    visit_type = models.CharField(null=True,max_length=100)
    visit_type_type = models.CharField(max_length=80, null=True)
    visit_type_value = models.CharField(max_length=40, null=True)
    visit_type_abbrev = models.CharField(max_length=20, null=True)
    visit_location = models.CharField(max_length=200, null=True)
    specialty = models.CharField(null=True, max_length=100)
    specialty_type = models.CharField(max_length=80, null=True)
    specialty_value = models.CharField(max_length=40, null=True)
    specialty_abbrev = models.CharField(max_length=20, null=True)
    signed_at = models.DateTimeField(null=True)
    provider_name = models.CharField(null=True,max_length=200)
    provider_institution = models.CharField(max_length=200, null=True)
    chief_complaint = models.CharField(null=True,max_length=255)
    content = models.TextField(null=True)


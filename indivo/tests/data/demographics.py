from indivo.models import Demographics
from base import ForeignKey, TestModel, scope

class TestDemographics(TestModel):
    # small subset of actual demographics info
    model_fields = ['name_family', 'name_given', 'bday', 'gender', 'email', 'document']
    model_class = Demographics

    def _setupargs(self, family_name, given_name, bday, gender, email=None, demographics_doc=None):
        self.name_family = family_name
        self.name_given = given_name
        self.bday = bday
        self.gender = gender
        self.email = email
        self.document = demographics_doc

_TEST_DEMOGRAPHICS = [
    {'family_name':'Wayne',
     'given_name': 'Bruce',
     'email': 'test@fake.org',
     'bday': '1939-11-15',
     'gender': 'male',
     'demographics_doc': ForeignKey('document', 'TEST_DEMOGRAPHICS_DOCS', 0)
     },
    {'family_name':'Testerson',
     'given_name': 'Test',
     'email': 'test2@fake.org',
     'bday': '1975-01-19',
     'gender': 'female',
     'demographics_doc': ForeignKey('document', 'TEST_DEMOGRAPHICS_DOCS', 1)
     },
    {'family_name':'McGee',
     'given_name': 'Testy',
     'email': 'test3@fake.org',
     'bday': '1985-06-01',
     'gender': 'female',
     'demographics_doc': ForeignKey('document', 'TEST_DEMOGRAPHICS_DOCS', 2)
     },
]
TEST_DEMOGRAPHICS = scope(_TEST_DEMOGRAPHICS, TestDemographics)
import string
from indivo.lib import utils
from indivo.models import Account
from base import TestModel, raw_data_to_objs

class TestAccount(TestModel):
    model_fields = ['email', 'full_name', 'contact_email', 'primary_secret', 'secondary_secret']
    model_class = Account

    def __init__(self, account_id, username, password, fullname='John Doe',
                 contact_email=None,
                 records=['jd','kid'],
                 primary_secret=utils.random_string(6, [string.digits]), 
                 secondary_secret=utils.random_string(6,[string.digits])):
        self.email = account_id
        self.username= username
        self.password = password
        self.full_name = fullname
        self.contact_email = contact_email if contact_email else self.account_id
        self.records = records if records else [fullname]
        self.primary_secret = primary_secret
        self.secodary_secret = secondary_secret
        self.build_django_obj()

_TEST_ACCOUNTS = [
    {'account_id':'stevezabak@informedcohort.org',
     'username': 'stevezabak',
     'password': 'abc',
     'fullname': 'Steve Zabak',
     'contact_email': 'steve.zabak@childrens.harvard.edu',
     'records': ['Steve Zabak'], 
     },
    {'account_id':'benadida@informedcohort.org',
     'username': 'benadida',
     'password': 'test',
     'fullname': 'Ben Adida',
     'contact_email': 'ben@adida.net',
     'records': ['Ben', 'R', 'M'],
     },
    {'account_id':'alice@childrens.harvard.edu', 
     'username': 'alice',
     'password': 'alice',
     'fullname': 'Alice Doe',
     'contact_email': 'contact@con.con',
     'records': ['the mom', 'the data', 'the son', 'the daughter'], 
     },
    {'account_id':'bob@childrens.harvard.edu',
     'username': 'bob',
     'password': 'robert',
     'fullname': 'Bob Doe',
     'contact_email': 'contact@con.con',
     'records': ['the mom', 'the data', 'the son', 'the daughter'], 
     },
    {'account_id':'mymail@mail.ma',
     'username': 'user',
     'password': 'pass',
     'fullname': 'full name',
     'contact_email': 'contact@con.con',
     'records': ['the mom', 'the data', 'the son', 'the daughter'], 
     'primary_secret': '010101',
     'secondary_secret': '010101'
     },
    ]

TEST_ACCOUNTS = raw_data_to_objs(_TEST_ACCOUNTS, TestAccount)

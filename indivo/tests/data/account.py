import random
from indivo.lib import utils

class TestAccount(object):
    def __init__(self, account_id, username, password, fullname='John Doe',
                 contact_email=None,
                 records=None,
                 primary_secret=utils.random_string(6, [string.digits]), 
                 secondary_secret=utils.random_string(6,[string.digits])):
        self.account_id = account_id
        self.username= username
        self.password = password
        self.fullname = fullname
        self.contact_email = contact_email if contact_email else self.account_id
        self.records = records if records else [fullname]
        self.primary_secret = primary_secret
        self.secodary_secret = secondary_secret

_TEST_ACCOUNTS = [
    {'account_id':'stevezabak@informedcohort.org',
     'username': 'stevezabak',
     'password': 'abc',
     'fullname': 'Steve Zabak',
     },
    {'account_id':'benadida@informedcohort.org',
     'username': 'benadida',
     'password': 'test',
     'fullname': 'Ben Adida'
     },
    {'account_id':'alice@childrens.harvard.edu', 
     'username': 'alice',
     'password': 'alice',
     'fullname': 'Alice Doe',
     },
    {'account_id':'bob@childrens.harvard.edu',
     'username': 'bob',
     'password': 'robert',
     'fullname': 'Bob Doe',
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

TEST_ACCOUNTS = [TestAccount(**raw_data) for raw_data in _TEST_ACCOUNTS]

from indivo.models import AuthSystem
from base import *

class TestAuthSystem(TestModel):
    model_fields = ['short_name', 'internal_p',]
    model_class = AuthSystem

    def _setupargs(self, short_name, internal_p=False):
        self.short_name = short_name
        self.internal_p = internal_p

_TEST_AUTHSYSTEMS = [
    {'short_name':'test_auth_system',
     'internal_p':False,
     },
    {'short_name':'test_auth_system2',
     'internal_p':False,
     },    
    ]
TEST_AUTHSYSTEMS = scope(_TEST_AUTHSYSTEMS, TestAuthSystem)

import django.test
from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.app import TEST_USERAPPS

class OauthInternalTests(InternalTests):
    
    def setUp(self):
        # This might not be sufficient: oauth might require reqTokens or Shares to be setup...
        # Should we even be testing oauth calls with accesscontrol disabled?
        super(OauthInternalTests,self).setUp(self)
        self.createAccount(TEST_ACCOUNTS, 4)
        self.createUserApp(TEST_USERAPPS, 0)

    def tearDown(self):
        super(OauthInternalTests,self).tearDown(self)


#oauth/access_token ['GET']
#oauth/authorize ['GET']
#oauth/internal/long-lived-token ['GET']
#oauth/internal/request_tokens/(?P<request_token>[^/]+)/approve ['GET']
#oauth/internal/request_tokens/(?P<request_token>[^/]+)/claim ['GET']
#oauth/internal/request_tokens/(?P<request_token>[^/]+)/info ['GET']
#oauth/internal/session_create ['GET']
#oauth/internal/surl-verify ['GET']
#oauth/request_token ['GET']

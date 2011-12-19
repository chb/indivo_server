from indivo.models import *
from indivo.tests.unit.models.base import TokenModelUnitTests
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.account import TEST_ACCOUNTS

class OauthInternalTests(TokenModelUnitTests):
    
    def setUp(self):
        super(OauthInternalTests,self).setUp()

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # A record for that account
        self.record = self.createRecord(TEST_RECORDS, 1, owner=self.account)

        # An app
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # A request token
        token, secret = self.generate_token_and_secret()
        args = {
            'token':token,
            'token_secret':secret,
            'verifier': self.generate_random_string(),
            'oauth_callback': self.app.callback_url,
            'pha': self.app,
            'record':self.record,
            'authorized_at':None,
            'authorized_by':None,
            'share':None
            }
        self.rt = ReqToken.objects.create(**args)

    def tearDown(self):
        super(OauthInternalTests,self).tearDown()


    def test_oauth_http_methods(self):
        invalid_calls = {
            '/oauth/request_token': ['get', 'put', 'delete'],
            '/oauth/access_token': ['get', 'put', 'delete'],
            '/oauth/internal/request_tokens/%s/info'%self.rt.token: ['put', 'post', 'delete'],
            '/oauth/internal/session_create': ['get', 'put', 'delete'],
            '/oauth/internal/request_tokens/%s/claim'%self.rt.token: ['get', 'put', 'delete'],
            '/oauth/internal/request_tokens/%s/approve'%self.rt.token: ['get', 'put', 'delete'],
            '/oauth/internal/surl-verify': ['put', 'post', 'delete'],
            }

        for url, invalid_methods in invalid_calls.iteritems():
            self.check_unsupported_http_methods(invalid_methods, url)

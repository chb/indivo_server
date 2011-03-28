import django.test
from indivo.models import *
from internal_tests import InternalTests

EMAIL, FULLNAME, CONTACT_EMAIL, USERNAME, PASSWORD, RECORDS = ("mymail@mail.ma","full name","contact@con.con","user","pass",("the mom", "the dad", "the son", "the daughter"))

class OauthInternalTests(InternalTests):
    
    def setUp(self):
        # This might not be sufficient: oauth might require reqTokens or Shares to be setup...
        # Should we even be testing oauth calls with accesscontrol disabled?
        super(OauthInternalTests,self).setUp(self)
        acct_args = {'email':EMAIL, 'full_name':FULLNAME, 'contact_email':CONTACT_EMAIL}
        self.createAccount(USERNAME, PASSWORD, RECORDS, **acct_args)

        pha_args = {'name' : 'myApp',
                     'email' : 'myApp@my.com',
                     'consumer_key' : 'myapp',
                     'secret' : 'myapp',
                     'has_ui' : True,
                     'frameable' : True,
                     'is_autonomous' : False,
                     'autonomous_reason' : '',
                     'start_url_template' : 'http://myapp.com/start',
                     'callback_url' : 'http://myapp.com/afterauth',
                     'description' : 'ITS MY APP',
                     'document_schema' : None
                     }
        self.createPHA(**pha_args)

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

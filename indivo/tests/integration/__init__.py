from app.main import Application
from indivo.tests.internal_tests import InternalTests
from test_modules.data import *

class IntegrationTests(InternalTests):

    def setUp(self):
        super(IntegrationTests, self).setUp()
        self.enableAccessControl()

        # Add the integration test apps
        pha_args = {'name' : 'User Test App', 
                    'email' : app_email, 
                    'consumer_key' : app_email, 
                    'secret' : app_secret, 
                    'has_ui' : True, 
                    'frameable' : True, 
                    'is_autonomous' : False, 
                    'autonomous_reason' : '', 
                    }
        self.createPHA(**pha_args)

        admin_args = {'name' : 'Chrome App', 
                      'email' : chrome_app_email, 
                      'consumer_key' : chrome_consumer_key, 
                      'secret' : chrome_consumer_secret,
                      'app_type': 'chrome',
                      }
        self.createAdminApp(**admin_args)

        admin_args = {'name' : 'Admin Test App', 
                      'email' : machine_app_email, 
                      'consumer_key' : machine_app_email,
                      'secret' : machine_app_secret,
                      'app_type': 'admin',
                      }
        self.createAdminApp(**admin_args)


        # Add the integration test accounts
        acct_args = {'email': 'benadida@informedcohort.org',
                     'full_name':'Ben',
                     'contact_email':'ben@adida.net',
                     }
        records = ['Ben', 'R', 'M']
        self.createAccount('benadida', 'test', records, **acct_args)

        acct_args = {'email': 'stevezabak@informedcohort.org',
                     'full_name':'Steve Zabak',
                     'contact_email':'steve.zabak@childrens.harvard.edu',
                     }
        records = ['Steve Zabak']
        self.createAccount('stevezabak', 'abc', records, **acct_args)

    def tearDown(self):
        super(IntegrationTests, self).tearDown()
        
    def test_integrations(self):
        app = Application()
        app.start()


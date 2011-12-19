from indivo.models import PHA, MachineApp, DocumentSchema
from base import *

class TestUserApp(TestModel):
    model_fields = ['name', 'email', 'consumer_key', 'secret', 'has_ui',
                    'frameable', 'is_autonomous', 'autonomous_reason',
                    'start_url_template', 'callback_url', 'description', 
                    'schema']
    model_class = PHA
    
    def _setupargs(self, name, email, consumer_key, secret, has_ui=True,
                 frameable=True, is_autonomous=False, autonomous_reason='', 
                 start_url_template='http://start', 
                 callback_url='http://afterauth',
                 description='An Indivo User App', schema=None):
        self.name = name
        self.email = email
        self.consumer_key = consumer_key
        self.secret = secret
        self.has_ui = has_ui
        self.frameable = frameable
        self.is_autonomous = is_autonomous
        self.autonomous_reason = autonomous_reason
        self.start_url_template = start_url_template
        self.callback_url = callback_url
        self.description = description
        try:
            self.schema = DocumentSchema.objects.get(type=schema)
        except DocumentSchema.DoesNotExist:
            self.schema = None

class TestMachineApp(TestModel):
    model_fields = ['name', 'email', 'consumer_key', 'secret', 'app_type']
    model_class = MachineApp
    
    def _setupargs(self, name, email, consumer_key, secret, app_type='admin'):
        self.name = name
        self.email = email
        self.consumer_key = consumer_key
        self.secret = secret
        self.app_type = app_type

_TEST_USERAPPS = [
    {'name' : 'myApp', 
     'email' : 'myApp@testapps.indivo.org', 
     'consumer_key' : 'myapp', 
     'secret' : 'myapp', 
     'has_ui' : True, 
     'frameable' : True, 
     'is_autonomous' : False, 
     'autonomous_reason' : '', 
     'start_url_template' : 'http://myapp.com/start', 
     'callback_url' : 'http://myapp.com/afterauth', 
     'description' : 'ITS MY APP',
     },
    {'name' : 'User Test App', 
     'email' : 'stephanie@apps.indivo.org', 
     'consumer_key' : 'stephanie@apps.indivo.org', 
     'secret' : 'norepinephrine', 
     'description' : 'USER TEST APP',
     },
    {'name' : 'User Test App2', 
     'email' : 'stephanie2@apps.indivo.org', 
     'consumer_key' : 'stephanie2@apps.indivo.org', 
     'secret' : 'norepinephrine2', 
     'description' : 'USER TEST APP 2',
     },
    ]
TEST_USERAPPS = scope(_TEST_USERAPPS, TestUserApp)

_TEST_AUTONOMOUS_APPS = [
    {'name' : 'myAutonomousApp', 
     'email' : 'myAutonomousApp@testapps.indivo.org', 
     'consumer_key' : 'myautonomousapp', 
     'secret' : 'myautonomousapp', 
     'has_ui' : True, 
     'frameable' : True, 
     'is_autonomous' : True, 
     'autonomous_reason' : 'Because I am the independent type.', 
     'start_url_template' : 'http://myautonomousapp.com/start', 
     'callback_url' : 'http://myapp.com/afterauth', 
     'description' : 'ITS MY AUTONOMOUS APP',
     },
    ]
TEST_AUTONOMOUS_APPS = scope(_TEST_AUTONOMOUS_APPS, TestUserApp)

_TEST_ADMINAPPS = [
    {'name' : 'Admin Test App', 
     'email' : 'stemapnea@apps.indivo.org', 
     'consumer_key' : 'stemapnea@apps.indivo.org', 
     'secret' : 'neuronagility', 
     'app_type' : 'admin',
     },
    {'name' : 'Admin Test App2', 
     'email' : 'stemapnea2@apps.indivo.org', 
     'consumer_key' : 'stemapnea2@apps.indivo.org', 
     'secret' : 'neuronagility2', 
     'app_type' : 'admin',
     },
    ]
TEST_ADMINAPPS = scope(_TEST_ADMINAPPS, TestMachineApp)

_TEST_UIAPPS = [
    {'name' : 'Chrome', 
     'email' : 'chrome@apps.indivo.org',
     'consumer_key' : 'chrome',
     'secret' : 'chrome', 
     'app_type' : 'chrome',
     },
    {'name' : 'OtherChrome', 
     'email' : 'ochrome@apps.indivo.org',
     'consumer_key' : 'ochrome',
     'secret' : 'ochrome', 
     'app_type' : 'chrome',
     },
    ]
TEST_UIAPPS = scope(_TEST_UIAPPS, TestMachineApp)

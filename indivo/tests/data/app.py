from indivo.models import PHA, MachineApp, DocumentSchema
from base import TestModel, raw_data_to_objs

class TestUserApp(TestModel):
    model_fields = ['name', 'email', 'consumer_key', 'secret', 'has_ui',
                    'frameable', 'is_autonomous', 'autonomous_reason',
                    'start_url_template', 'callback_url', 'description', 
                    'schema']
    model_class = PHA
    
    def __init__(self, name, email, consumer_key, secret, has_ui=True,
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
        if schema:
            try:
                self.schema = DocumentSchema.objects.get(type=schema)
            except DocumentSchema.DoesNotExist:
                self.schema = None
        self.build_django_obj()

class TestMachineApp(TestModel):
    model_fields = ['name', 'email', 'consumer_key', 'secret', 'app_type']
    model_class = MachineApp
    
    def __init__(self, name, email, consumer_key, secret, app_type='admin'):
        self.name = name
        self.email = email
        self.consumer_key = consumer_key
        self.secret = secret
        self.app_type = app_type
        self.build_django_obj()


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
    ]

_TEST_AUTONOMOUS_APPS = []

_TEST_ADMINAPPS = [
    {'name' : 'Admin Test App', 
     'email' : 'stemapnea@apps.indivo.org', 
     'consumer_key' : 'stemapnea@apps.indivo.org', 
     'secret' : 'neuronagility', 
     'app_type' : 'admin',
     },
    ]

_TEST_UIAPPS = [
    {'name' : 'Chrome', 
     'email' : 'chrome@apps.indivo.org',
     'consumer_key' : 'chrome',
     'secret' : 'chrome', 
     'app_type' : 'chrome',
     },
    ]

TEST_USERAPPS = raw_data_to_objs(_TEST_USERAPPS, TestUserApp)
TEST_AUTONOMOUS_APPS = raw_data_to_objs(_TEST_AUTONOMOUS_APPS, TestUserApp)
TEST_ADMINAPPS = raw_data_to_objs(_TEST_ADMINAPPS, TestMachineApp)
TEST_UIAPPS = raw_data_to_objs(_TEST_UIAPPS, TestMachineApp)

from indivo.models import PHA, MachineApp
from base import *

class TestUserApp(TestModel):
    model_fields = ['name', 'email', 'consumer_key', 'secret', 'author',
                    'has_ui', 'version', 'indivo_version', 'icon_url',
                    'frameable', 'is_autonomous', 'autonomous_reason',
                    'start_url_template', 'callback_url', 'description',
                    'requirements',]
    model_class = PHA
    
    def _setupargs(self, name, email, consumer_key, secret, author='testauthor',
                   has_ui=True, version='1.0.0', indivo_version='1.0.0',
                   icon_url='http://myicons.com/icon.png',
                   frameable=True, is_autonomous=False, autonomous_reason='', 
                   start_url_template='http://start', 
                   callback_url='http://afterauth',
                   description='An Indivo User App',
                   requirements='{}'):
        self.name = name
        self.email = email
        self.consumer_key = consumer_key
        self.secret = secret
        self.author = author
        self.has_ui = has_ui
        self.version = version
        self.indivo_version = indivo_version
        self.icon_url = icon_url
        self.frameable = frameable
        self.is_autonomous = is_autonomous
        self.autonomous_reason = autonomous_reason
        self.start_url_template = start_url_template
        self.callback_url = callback_url
        self.description = description
        self.requirements = requirements

class TestMachineApp(TestModel):
    model_fields = ['name', 'email', 'consumer_key', 'secret', 
                    'description', 'author', 'version', 'indivo_version',
                    'app_type']
    model_class = MachineApp
    
    def _setupargs(self, name, email, consumer_key, secret, 
                   description= "An Indivo Machine App",
                   author="testauthor", version="1.0.0", 
                   indivo_version="1.0.0", app_type='admin'):
        self.name = name
        self.email = email
        self.consumer_key = consumer_key
        self.secret = secret
        self.description = description
        self.author = author
        self.version = version
        self.indivo_version = indivo_version
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

TEST_SMART_MANIFESTS = [
('''
{
    "name" : "SMART TEST Problems",
    "description" : "Display problems in a table view",
    "author" : "Josh Mandel, Children's Hospital Boston",
    "id" : "problem-list-test@apps.smartplatforms.org",
    "version" : ".1a",

    "mode" : "ui",
    "scope": "record",

    "index" : "http://fda.gping.org:8012/framework/problem_list/index.html",	
    "icon" : "http://fda.gping.org:8012/framework/problem_list/icon.png",
  
    "requires" : {
        "http://smartplatforms.org/terms#Problem": {
            "methods": ["GET"]
        }
    }
}
''',
'''
{
    "consumer_key": "problem-list-test@apps.indivo.org",
    "consumer_secret": "problemstest"
}
'''),
]

TEST_USERAPP_MANIFESTS = [
('''
{
  "name" : "Problems TEST",
  "description" : "Display a list of problems, or enter new ones.",
  "author" : "Arjun Sanyal, Children's Hospital Boston",
  "id" : "problemstest@apps.indivo.org",
  "version" : "1.0.0",
  "smart_version": "0.4",

  "mode" : "ui",	
  "scope": "record",
  "has_ui": true,
  "frameable": true,

  "icon" :  "jmvc/ui/resources/images/app_icons_32/problems.png",
  "index": "/apps/problems/start_auth?record_id={record_id}&amp;carenet_id={carenet_id}",
  "oauth_callback_url": "/apps/problems/after_auth"
}
''',
'''
{
    "consumer_key": "problemstest@apps.indivo.org",
    "consumer_secret": "problemstest2"
}
'''),
]

TEST_ADMINAPP_MANIFESTS = [
('''
{
    "name": "Sample Admin App Test",
    "description" : "The reference Indivo UI App",
    "author" : "Ben Adida, Travers Franckle, Arjun Sanyal, Pascal Pfiffner, Daniel Haas. Children's Hospital Boston",
    "id" : "sample_admin_app_test@apps.indivo.org",
    "version" : "2.0.0",
    "indivo_version": "2.0.0",
    "ui_app": false
}
''',
'''
{
    "consumer_key": "sampleadmin_key_test",
    "consumer_secret": "sampleadmin_secret_test"
}
'''),
]

TEST_UIAPP_MANIFESTS = [
('''
{
    "name": "Sample UI App Test",
    "description" : "The reference Indivo UI App",
    "author" : "Ben Adida, Travers Franckle, Arjun Sanyal, Pascal Pfiffner, Daniel Haas. Children's Hospital Boston",
    "id" : "chrome_test@apps.indivo.org",
    "version" : "2.0.0",
    "indivo_version": "2.0.0",
    "ui_app": true
}
''',
'''
{
    "consumer_key": "chrome_test",
    "consumer_secret": "chrome_test"
}
'''),
]

'''
Old Code for autoloading test classes

def get_test_modules(): 
    from os import path, listdir 
    names = set() 
    for f in listdir(path.dirname(__file__)): 
        if f.startswith('.') or f.startswith('__') or f.endswith('.pyc'): 
            continue 
        names.add(f.split('.')[0]) 
    for name in names: 
        yield (name, __import__('%s.%s' % (__name__, name), {}, {}, [''])) 

def setup_unit_tests(): 
    import django.test, unittest
    for name, module in get_test_modules(): 
        # Import each TestCase from the current module. 
        for k, v in module.__dict__.iteritems():             
            if ( isinstance(v, type) and issubclass(v, django.test.TestCase) ) or \
                    ( isinstance(v, type) and issubclass(v, unittest.TestCase) ):                 
                globals()[k] = v 

setup_unit_tests()
'''

#Internal Tests
from accounts_tests import AccountInternalTests
from apps_tests import PHAInternalTests
from carenets_tests import CarenetInternalTests
from oauth_tests import OauthInternalTests
from records_tests import RecordInternalTests
from reporting_tests import ReportingInternalTests

#Unit Tests
#from unittests import *


__all__ = ['Application', 'IndivoClient', 'IndivoClientError']

# System
import sys, os, urllib

# Application
TEST_MODULES_DIR_LOC = os.path.abspath(os.path.dirname(__file__)) + '/../test_modules'
path_lib = os.path.abspath(os.path.dirname(__file__)) + '/../indivo_client_py/lib'

# Client 
try:
  from indivo.tests.client.lib.client import IndivoClient, IndivoClientError
except ImportError:
  raise Exception("Client tests needs to be included as a submodule within the indivo client")

import functools

# API
import inspect
import traceback

from indivo.tests.integration.config  import ts
from progress_bar     import ProgressBar

PRD = 'prd' 
PASS, FAIL = 'pass', 'fail'
ERR, RESULT, TRACEBACK =  ('err', 'result', 'traceback')

class Application():

  def start(self):
    welcome = '''
==========================
RUNNING INTEGRATION TESTS:
==========================
'''
    print welcome
    count = 0
    report = {}
    progress = ProgressBar(0, len(ts), 77)
    modules = self.load_modules()
    for test_block in ts:
      name, func, test =  (test_block['name'], test_block['func'], test_block['test'])
      progress(count)
      if test:
        report = self.report_setup(name, report)
        try:
          self.run_test(func, modules)
        except Exception, e:
          report = self.report_exception(name, report, e)
      count += 1
    self.display_report(report)
    return True

  def report_setup(self, name, report):
    report[name]          = {}
    report[name][RESULT]  = PASS
    report[name][ERR]     = ''
    return report

  def report_exception(self, name, report, e):
    report[name][RESULT]  = FAIL
    report[name][ERR]     = e
    if hasattr(e, 'msg'):
      report[name][ERR] = e.msg
      if isinstance(e.msg, dict) and \
        e.msg.has_key(PRD):
        report[name][ERR] = e.msg[PRD]
    if hasattr(e, TRACEBACK):
      report[name][TRACEBACK] = e.traceback
    return report

  def load_modules(self):
    modules = []
    exceptions = ['__init__.py', 'data.py']
    files = [file[0:-3] for file in os.listdir(TEST_MODULES_DIR_LOC) \
                  if  file[-3:] != 'pyc' and file not in exceptions and \
                      file[0] != '.' and file[-1] != '~' and file[-1] != '#']
    sys.path.insert(0, os.path.abspath(TEST_MODULES_DIR_LOC))
    for file in files:
      if file:
        try:
          modules.append(__import__(file))
        except ImportError:
          pass
    return modules

  def run_test(self, func, modules):
    for module in modules:
      if hasattr(module, func):
        res = getattr(module, func)(IndivoClient)
        if isinstance(res, bool):
          if res != True:
            raise Exception 
          return True
        elif isinstance(res, tuple):
          if not res[0]:
            raise IndivoClientError(res[1])
    return False

  def display_report(self, report):
    divider = 77*'='
    print divider
    print "Report:"
    for name, info in report.items():
      result = info[RESULT]
      print 10*'.', result + ' : ' + name
      if result == FAIL:
        print 20*'.', info[ERR]
        if info.has_key(TRACEBACK):
          print 20*'.', info[TRACEBACK][1][3]
    print divider

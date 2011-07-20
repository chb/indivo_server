"""
Pull relevant info from the indivo_server codebase to generate a framework for Indivo documentation
"""

from django.core.management.base import BaseCommand, CommandError
from operator import attrgetter
from indivo.accesscontrol.access_rule import AccessRule
import indivo
import urls
import re

class Command(BaseCommand):
    args = ''
    help = 'Generate a Framework for the Indivo Documentation'

    def handle(self, *args, **options):
        cp = CallParser(urls.urlpatterns)
        print cp

class Call(object):
    def __init__(self, path, method, view_func, access_rule=None):
        self.path = path
        self.method = method
        self.view_func = view_func
        self.view_func_name = view_func.__name__
        self.access_rule = access_rule or self._get_access_rule()
        self.access_doc = self.access_rule.rule.__doc__ if self.access_rule else None
        
    def __str__(self):
        return "%s %s: %s, access=%s"%(self.method, self.path, self.view_func_name, self.access_doc)

    def _get_access_rule(self):
        return AccessRule.lookup(self.view_func)

class CallParser(object):
    def __init__(self, urls):
        self.urllist = urls
        self.paths = {}
        self.parse(self.urllist, parent_path='/')
        self.sorted_calls = sorted(self.paths.values(), key=attrgetter('path', 'method'))

    def __str__(self):
        return '\n'.join([str(c) for c in self.sorted_calls])

    def register(self, call):
        self.paths['%s %s'%(call.method, call.path)] = call

    def lookup(self, call):
        return self.paths['%s %s'%(call.method, call.path)]

    def parse(self, urllist, parent_path=''):
        for entry in urllist:
                
            # not a leaf node, recurse
            if hasattr(entry, 'url_patterns'):
                cur_path = entry.regex.pattern[1:]
                self.parse(entry.url_patterns, parent_path+cur_path)
                    
            # leaf node
            else:
                path = self.parse_url_params(parent_path + entry.regex.pattern[1:-1])
                if isinstance(entry.callback, indivo.lib.utils.MethodDispatcher):
                    for method, view_func in entry.callback.methods.iteritems():
                        call = Call(path, method, view_func=view_func)
                        self.register(call)
                else:
                    method = 'GET'
                    call = Call(path, method, entry.callback)
                    self.register(call)

    def parse_url_params(self, url):
        # match things inside <> that are in the context of (?P< your match >..) 
        for pattern in re.finditer( '\(\?P<(.*?)>.*?\)', url):
            url = url.replace(pattern.group(0), '{%s}'%pattern.group(1).upper())
        return url

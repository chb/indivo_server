"""
Pull relevant info from the indivo_server codebase to generate a framework for Indivo documentation
"""

from django.core.management.base import BaseCommand, CommandError
from indivo_server.doc.sphinx.autogen.api_parser import APIDict, CallParser, CallResolver, Call
from indivo_server.doc.sphinx.autogen.api_defaults import *
from django.conf import settings
import urls
import os

class Command(BaseCommand):
    args = 'parse | build'
    help = '''\
generate_docs: Generate a Framework for the Indivo API Documentation. 

Workflow is as follows:

* Run ``./manage.py generate_docs parse``, which pulls in the latest Indivo code
  to create an up-to-date skeleton listing of all API calls supported by Indivo.
  This skeleton is written to a file specified by api_parser.py, usually 
  'api-skeleton.py' in this directory.

* Edit the skeleton file, adding call descriptions, querystring options, url
  parameters, etc. Descriptions may be written as ReST, as they will be plugged
  directly into the Sphinx documentation. The state that you leave this file in 
  will be authoritative until you call ``./manage.py generate_docs parse`` again 
  to re-parse the codebase. Make sure that you this file's syntax is valid Python 
  (i.e., quote all strings appropriately).

* Run ``./manage.py generate_docs build``, which compiles the sphinx documentation,
  using the skeleton file as a reference for the API. 

* Continue to edit the skeleton file or the documentation itself and re-run
  ``./manage.py generate_docs build`` as often as you like. If the code changes,
  make sure to re-run ``./manage.py generate_docs parse`` to pull those changes
  into the skeleton file.
'''

    userfields = ['query_opts', 'data_fields', 'description', 'return_desc', 
                  'return_ex', 'deprecated', 'added', 'changed']
    cpfields = ['method', 'path', 'view_func_name', 'url_params', 'access_doc']
    
    defaults_map = {
        'url_params': URL_PARAM_DESC,
        'query_opts': QUERY_PARAM_DESC,
        'data_fields': DATA_FIELD_DESC,
        'description': TEXT_FIELD_DESC,
        'return_desc': TEXT_FIELD_DESC,
        'return_ex': TEXT_FIELD_DESC,
        }

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Expected exactly 1 argument: "parse" or "build"')

        if args[0] == 'parse':

            # Parse the indivo server codebase for the latest API calls
            cp = CallParser(urls.urlpatterns)
            cp_api = cp.api
            
            # Get the current user-modified listing of calls
            user_api = APIDict()
            
            # Init a new listing for update
            new_api = APIDict(read_file=False)

            # Diff them
            cp_set = set(cp_api.keys())
            user_set = set(user_api.keys())
        
            intersection = cp_set & user_set
            cp_only = cp_set - user_set
            user_only = user_set - cp_set

            diffstr = 'Changed calls:\n'

            # Calls in both versions
            for title in intersection:
                modified = False
                user_call = user_api[title]
                cp_call = cp_api[title] 
                new_call = Call()
                resolver = CallResolver(cp_call, user_call)
                mod = False

                # computerized fields: choose codebase version, default to user if codebase didn't have it.
                resolver.prefer_cp()
                for field in self.cpfields:
                    oldval = getattr(user_call, field, None)
                    defaults = self.defaults_map.get(field, None)
                    newval = resolver.resolve(field, defaults)
                    setattr(new_call, field, newval)
                    if oldval != newval:
                        mod = True

                # user fields: choose user version, default to codebase if user hasn't entered it.
                resolver.prefer_user()
                for field in self.userfields:
                    oldval = getattr(user_call, field, None)
                    defaults = self.defaults_map.get(field, None)
                    newval = resolver.resolve(field, defaults)
                    setattr(new_call, field, newval)
                    if oldval != newval:
                        mod = True

                # Note: a 'modified' call is one that has had computerized values
                # written over whatever existed in api-skeleton.py.
                if mod:
                    diffstr += 'MOD: %s\n'%title

                new_api.update({title:new_call})

            # Calls in just the cp version are new: add them to the userfile
            for title in cp_only:
                new_api.update({title:cp_api[title]})
                new_api[title].set_defaults(self.defaults_map)
                diffstr += 'ADD: %s\n'%title

            # Calls in just the userfile are no longer valid: delete them from the userfile
            for title in user_only:
                diffstr += 'DEL: %s\n'%title # no need to touch the new_api, since it doesn't contain the call

            # Write our changes out to the userfile
            new_api.save()

            # Print out a diff of what got added and deleted: can't print mods because we don't store past history
            print diffstr

        elif args[0] == 'build':
            
            # generate the api reference
            APIDict().write_ReST_reference()

            # Use sphinx-apidoc to autogenerate code docs
            exclude_paths = [
                settings.APP_HOME + '/doc/',
                settings.APP_HOME + '/codingsystems/migrations/',
                settings.APP_HOME + '/codingsystems/urls/',
                settings.APP_HOME + '/indivo/migrations/',
                settings.APP_HOME + '/indivo/urls/',
                ]

            output_dir = 'source/autocode'
            source_dir = settings.APP_HOME
            
            cmd = 'sphinx-apidoc -o %s %s %s'%(output_dir, 
                                               source_dir, 
                                               ' '.join(exclude_paths))

            os.chdir(settings.APP_HOME+'/doc/sphinx')
            ret = os.system(cmd)

            # Build the Docs
            ret = os.system('make html')

        else:
            raise CommandError('Unexpected argument: %s. Expected 1 argument: "parse" or "build"'%args[0])            

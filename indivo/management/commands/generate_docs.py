"""
Pull relevant info from the indivo_server codebase to generate a framework for Indivo documentation
"""

from django.core.management.base import BaseCommand, CommandError
from doc.sphinx.autogen.api_parser import APIDict, CallParser, CallResolver, Call
from doc.sphinx.autogen.api_defaults import *
from django.conf import settings
import urls
import os
import copy

class Command(BaseCommand):
    args = 'parse | build | prepare'
    help = '''\
generate_docs: Generate a Framework for the Indivo API Documentation. 

Workflow is as follows:

* Run ``./manage.py generate_docs parse``, which pulls in the latest Indivo code
  to create an up-to-date skeleton listing of all API calls supported by Indivo.
  This skeleton is written to a file specified by api_parser.py, usually 
  ``indivo_server/doc/sphinx/autogen/api-skeleton.py``.

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

Additionally, for readthedocs.org support, the ``prepare`` argument will do all the
prep work except the final call to build the docs.

'''

    userfields = ['query_opts', 'data_fields', 'return_desc', 
                  'return_ex', 'deprecated', 'added', 'changed']
    cpfields = ['method', 'path', 'view_func_name', 'url_params', 'access_doc',
                'description']
    
    defaults_map = {
        'url_params': URL_PARAM_DESC,
        'query_opts': QUERY_PARAM_DESC,
        'data_fields': DATA_FIELD_DESC,
        'description': TEXT_FIELD_DESC,
        'return_desc': TEXT_FIELD_DESC,
        'return_ex': TEXT_FIELD_DESC,
        }

    autocode_exclude_paths = [
                
        # Always exclude these
        settings.APP_HOME + '/indivo/migrations/',
        settings.APP_HOME + '/indivo/urls/',
        settings.APP_HOME + '/indivo/templates/',
        settings.APP_HOME + '/indivo/tests/',
        
        # Excluded for now, add back in as they get documented
        settings.APP_HOME + '/indivo/accesscontrol/',
        settings.APP_HOME + '/indivo/document_processing/',
        settings.APP_HOME + '/indivo/lib/',
        settings.APP_HOME + '/indivo/management/',
        settings.APP_HOME + '/indivo/middlewares/',
        settings.APP_HOME + '/indivo/models/',
        settings.APP_HOME + '/indivo/templatetags/',
        ]

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Expected exactly 1 argument: "parse", "build", or "prepare"')

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
                    newval = resolver.resolve(field)
                    setattr(new_call, field, newval)
                    if oldval != newval:
                        mod = True

                # user fields: choose user version, default to codebase if user hasn't entered it.
                resolver.prefer_user()
                for field in self.userfields:
                    oldval = getattr(user_call, field, None)
                    newval = resolver.resolve(field)
                    setattr(new_call, field, newval)
                    if oldval != newval:
                        mod = True


                # Set defaults for values that weren't in the cp_call or the user_call
                mod = new_call.set_defaults(self.defaults_map)

                # Note: a 'modified' call is one that has had computerized values
                # written over whatever existed in api-skeleton.py.
                if mod:
                    diffstr += 'MOD: %s\n'%title

                new_api.update({title:new_call})

            # Calls in just the cp version are new: add them to the userfile
            for title in cp_only:
                new_call = copy.copy(cp_api[title])
                new_call.set_defaults(self.defaults_map)                
                new_api.update({title:new_call})
                diffstr += 'ADD: %s\n'%title

            # Calls in just the userfile are no longer valid: delete them from the userfile
            for title in user_only:
                diffstr += 'DEL: %s\n'%title # no need to touch the new_api, since it doesn't contain the call

            # Write our changes out to the userfile
            new_api.save()

            # Print out a diff of what got added and deleted: can't print mods because we don't store past history
            print diffstr

        elif args[0] == 'build':
            api = APIDict()
            
            # Write the API Reference ReST doc
            self.write_api_reference(api)

            # Write the Python Client Reference ReST doc
            self.write_client_reference(api)
            
            # Use sphinx-apidoc to autogenerate code docs
            self.build_autocode()

            # Build the Docs
            self.build_docs()

        elif args[0] == 'prepare':
            api = APIDict()
            
            # Write the API Reference ReST doc
            self.write_api_reference(api)
            
            # Write the Python Client Reference ReST doc
            self.write_client_reference(api)

            # Use sphinx-apidoc to autogenerate code docs
            self.build_autocode()

            # Don't Build the Docs

        else:
            raise CommandError('Unexpected argument: %s. Expected 1 argument: "parse" or "build"'%args[0])            

    def write_api_reference(self, api):
        api.write_ReST_reference()

    def write_client_reference(self, api):
        api.write_python_client_reference()

    def build_autocode(self):
        output_dir = 'source/autocode'
        source_dir = settings.APP_HOME + '/indivo/'
        
        cmd = 'sphinx-apidoc -o %s %s %s'%(output_dir,
                                           source_dir, 
                                           ' '.join(self.autocode_exclude_paths))
        self.chdir_and_execute(settings.APP_HOME+'/doc/sphinx', cmd)

    def build_docs(self):
        cmd = 'make html SPHINXOPTS=-a'
        self.chdir_and_execute(settings.APP_HOME+'/doc/sphinx', cmd)

    def chdir_and_execute(self, dir, cmd):
        """ Move to a directory, execute a shell command, then move back out. """
        old_dir = os.getcwd()
        os.chdir(dir)
        ret = os.system(cmd)
        os.chdir(old_dir)
        return ret

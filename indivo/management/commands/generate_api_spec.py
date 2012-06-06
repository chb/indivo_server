"""
Pull relevant info from the indivo_server codebase to generate a framework for Indivo documentation
"""

from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError
from doc.sphinx.autogen.api_parser import APIDict, CallParser, CallResolver, Call
from django.conf import settings
import urls
import os
import copy

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-o', '--output-file',
                    action='store', type='string', dest='output_file',
                    default='', help='Full path to the location to write the API spec.'),
        )
    help = '''\
generate_api_spec: Generate a Specification of the Indivo API.

The specification takes the form of a simple XML File, which looks like:

<api>
  <call name="get_version", method="get", url="/version" />
  <call name="document_create", method="post", url="/records/{RECORD_ID}/documents/ />
      ... More calls ...
</api>

This XML file will be written to disk at indivo_server/api.xml, unless overridden by the -o flag.
'''

    def handle_noargs(self, **options):
        # Parse the indivo server codebase for the latest API calls
        cp = CallParser(urls.urlpatterns)

        # Write the API calls as an XML spec
        cp.api.write_api_spec(options.get('output_file', ''))


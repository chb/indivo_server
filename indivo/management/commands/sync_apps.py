"""
remove accesstokens and sessiontokens that are expired.
"""


from django.core.management.base import BaseCommand, CommandError
from utils.importer import AppSyncer

class Command(BaseCommand):
    args = ''
    help = 'Sync the currently registered apps with settings.APPS_DIRS'

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        
        def print_if(stmt, min_verbosity=1):
            if verbosity > min_verbosity:
                print stmt
                
        print_if("Importing currently registered apps...")
        AppSyncer().sync(verbosity)
        print_if("Done.")

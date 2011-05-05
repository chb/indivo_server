"""
Drop and Re-parse facts from indivo documents. Should be wrapped around a migration
"""

from django.core.management.base import BaseCommand, CommandError
from indivo.document_processing.document_processing import DocumentProcessing
from indivo.models import Document, Fact

class Command(BaseCommand):
    args = 'drop | process'
    help = 'Reset Fact objects in the Indivo database before Migration. "drop" \
removes all objects, and "process" re-processes existing documents to create new objects'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Expected 1 argument: "drop" or "process"')
        
        if args[0] == 'drop':
            print "Deleting all existing Fact Objects..."
            Fact.objects.all().delete()
            print "Done."
        elif args[0] == 'process':
            print "Re-processing all Documents..."
            for doc in Document.objects.all():
                
                # only reprocess the most recent version of docs
                if not doc.replaced_by:
                    doc.processed = False                
                    doc.save()
            print "Done."
        else:
            raise CommandError('Invalid argument: %s. Expected "drop" or "process"'%args[0])

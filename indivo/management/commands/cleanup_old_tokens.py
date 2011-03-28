"""
remove accesstokens and sessiontokens that are expired.
"""


from django.core.management.base import BaseCommand, CommandError
import datetime
from indivo.models import *

class Command(BaseCommand):
    args = ''
    help = 'clean up old session and access tokens'

    def handle(self, *args, **options):
        now = datetime.datetime.utcnow()

        # remove old access tokens
        SessionToken.objects.filter(expires_at__lt = now).delete()

        # remove old session tokens
        AccessToken.objects.filter(expires_at__lt = now).delete()

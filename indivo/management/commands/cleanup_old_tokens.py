"""
remove accesstokens and sessiontokens that are expired.
"""


from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from indivo.models import *
from oauth.oauth import TIMESTAMP_THRESHOLD

class Command(BaseCommand):
    args = ''
    help = 'clean up old session and access tokens'

    def handle(self, *args, **options):
        now = timezone.now()
        max_delta = datetime.timedelta(seconds=TIMESTAMP_THRESHOLD)
        oldest_nonce = now - max_delta

        # remove old access tokens
        SessionToken.objects.filter(expires_at__lt = now).delete()

        # remove old session tokens
        AccessToken.objects.filter(expires_at__lt = now).delete()

        # remove old Nonces
        Nonce.objects.filter(created_at__lt = oldest_nonce).delete()

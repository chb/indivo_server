
"""
Indivo Model for healthfeed
"""

from django.db import models
from django.conf import settings

from base import Object, Principal, INDIVO_APP_LABEL

class Notification(Object):
  account = models.ForeignKey('Account')
  record = models.ForeignKey('Record', null = True)
    
  # someone sends a notification to an account, pertaining to a record
  sender = models.ForeignKey('Principal', related_name = 'notifications_sent_by')

  # the text of the notification
  content = models.CharField(max_length= 500)
    
  # the document ID this pertains to
  document = models.ForeignKey('Document', null = True)

  # the URL to the PHA for followup
  app_url = models.CharField(max_length=300, null = True)


class RecordNotificationRoute(Object):
  record = models.ForeignKey('Record', related_name = 'notification_routes')
    
  # account to which notifications are routed
  account = models.ForeignKey('Account')
  
  class Meta:
    app_label = INDIVO_APP_LABEL
    unique_together = (('account', 'record'),)

"""
.. module:: views.messaging
   :synopsis: Indivo view implementations for messaging-related calls.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from base import *

import datetime

import markdown
from indivo.lib import mdx_linkexpander
from django.db import IntegrityError

def _get_subject(request):
  """Extract a message subject from request.POST."""

  subject = []
  subject.append(request.POST.get('subject', "[no subject]"))
  return ''.join(subject)

@transaction.commit_on_success
@handle_integrity_error('Duplicate external id. Each message requires a unique message_id')
def account_send_message(request, account):
  """ Send a message to an account.

  Account messages have no attachments for now, as we wouldn't know
  which record to store them on.

  request.POST may contain any of:

  * *message_id*: An external identifier for the message, used for later
    retrieval. Defaults to ``None``.

  * *body*: The message body. Defaults to ``[no body]``.

  * *severity*: The importance of the message. Options are ``low``, ``medium``,
    ``high``. Defaults to ``low``.

  After delivering the message to Indivo's inbox, this call will send an email to 
  the account's contact address, alerting them that a new message has arrived.

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if the
  passed *message_id* is a duplicate.
  
  """

  Message.objects.create( 
    account             = account, 
    sender              = request.principal, 
    recipient           = account, 
    external_identifier = request.POST.get('message_id', None), 
    subject             = _get_subject(request),
    body                = request.POST.get('body', "[no body]"),
    severity            = request.POST.get('severity', 'low'))
  
  account.notify_account_of_new_message()
  return DONE

@transaction.commit_on_success
@handle_integrity_error('Duplicate external id. Each message requires a unique message_id')
def record_send_message(request, record, message_id):
  """ Send a message to a record.

  request.POST may contain any of:

  * *body*: The message body. Defaults to ``[no body]``.

  * *body_type*: The formatting of the message body. Options are ``plaintext``,
    ``markdown``. Defaults to ``markdown``.

  * *num_attachments*: The number of attachments this message requires. Attachments
    are uploaded with calls to 
    :py:meth:`~indivo.views.messaging.record_message_attach`, and 
    the message will not be delivered until all attachments have been uploaded.
    Defaults to 0.

  * *severity*: The importance of the message. Options are ``low``, ``medium``,
    ``high``. Defaults to ``low``.

  After delivering the message to the Indivo inbox of all accounts authorized to
  view messages for the passed *record*, this call will send an email to each 
  account's contact address, alerting them that a new message has arrived.

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if the
  passed *message_id* is a duplicate.
  
  """

  record.send_message(
    external_identifier = message_id, 
    sender              = request.principal.effective_principal,
    subject             = _get_subject(request),
    body                = request.POST.get('body',    '[no body]'),
    body_type           = request.POST.get('body_type',    'plaintext'),
    num_attachments     = request.POST.get('num_attachments', 0),
    severity            = request.POST.get('severity', 'low'))
  
  return DONE

@transaction.commit_on_success
@handle_integrity_error('Duplicate attachment number. Each attachment number must be unique and 1-indexed')
def record_message_attach(request, record, message_id, attachment_num):
  """ Attach a document to an Indivo message.

  Only XML documents are accepted for now. Since Message objects are duplicated
  for each recipient account, this call may attach the document to multiple
  Message objects.

  request.POST must contain the raw XML attachment data.

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if the
  attachment with number *attachment_num* has already been uploaded.

  """

  # there may be more than one message here
  messages = Message.objects.filter(about_record = record, external_identifier = message_id)
  
  for message in messages:
    message.add_attachment(attachment_num, request.raw_post_data)

  return DONE

@marsloader()
def account_inbox(request, account, limit, offset, status, order_by):
  """ List messages in an account's inbox.

  Messages will be ordered by *order_by* and paged by *limit* and
  *offset*. request.GET may additionally contain:

  * *include_archive*: Adds messages that have been archived (which are
    normally omitted) to the listing. Any value will be interpreted as ``True``. 
    Defaults to ``False``, as if it weren't passed.

  Will return :http:statuscode:`200` with a list of messages on success.

  """

  messages = account.message_as_recipient.order_by(order_by)

  if not request.GET.get('include_archive', False):
    messages = messages.filter(archived_at=None)

  return render_template('messages', {'messages' : messages})


def account_inbox_message(request, account, message_id):
  """ Retrieve an individual message from an account's inbox.

  This call additionally filters message content based on its
  body-type. For example, markdown content is scrubbed of 
  extraneous HTML, then converted to HTML content. Also, this
  call marks the message as read.

  *message_id* should be the external identifier of the message
  as created by 
  :py:meth:`~indivo.views.messaging.account_send_message` or
  :py:meth:`~indivo.views.messaging.record_send_message`.

  Will return :http:statuscode:`200` with XML describing the message
  (id, sender, dates received, read, and archived, subject, body,
  severity, etc.) on success.

  """

  message = account.message_as_recipient.get(id = message_id)

  # if message not read, mark it read
  if not message.read_at:
    message.read_at = datetime.datetime.utcnow()
    message.save()

  # markdown
  if message.body_type == 'markdown':
    ext = mdx_linkexpander.MessageLinkExpanderExtension({
        'APP_BASE':'foobar',
        'message_id': message_id
        })
    message.body = markdown.Markdown(safe_mode=True, output_format='html4', extensions = [ext]).convert(message.body)

  return render_template('message', {'message' : message})


def account_inbox_message_attachment_accept(request, account, message_id, attachment_num):
  """ Accept a message attachment into the record it corresponds to.

  This call is triggered when a user views a message with an attachment, and 
  chooses to add the attachment contents into their record.

  Will return :http:statuscode:`200` on success, :http:statuscode:`410` if the 
  attachment has already been saved.

  """
  message = account.message_as_recipient.get(id = message_id)
  
  # this might fail, if the document doesn't validate
  try:
    message.get_attachment(int(attachment_num)).save_as_document(account)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
  else:
    return DONE

def account_message_archive(request, account, message_id):
  """ Archive a message.

  This call sets a message's archival date as now, unless it's already set. 
  This means that future calls to 
  :py:meth:`~indivo.views.messaging.account_inbox` will not
  display this message by default.
  
  Will return :http:statuscode:`200` on success.

  """

  message = account.message_as_recipient.get(id = message_id)
  if not message.archived_at:
    message.archived_at = datetime.datetime.utcnow()
    message.save()
  return DONE


@marsloader()
def account_notifications(request, account, limit, offset, status, order_by):
  """ List an account's notifications.

  Orders by *order_by*, pages by *limit* and *offset*.
  
  Will return :http:statuscode:`200` with a list of notifications on success.

  """

  notifications = Notification.objects.filter(account = account).order_by(order_by)
  return render_template('notifications', {'notifications' : notifications})

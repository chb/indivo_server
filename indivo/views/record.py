"""
.. module: views.record
   :synopsis: Indivo view implementations for record-related calls.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

#import libxml2
from lxml import etree

from indivo.lib import utils
from indivo.views.documents.document import _document_create
from base import *

ACTIVE_STATE = 'active'



@marsloader()
def record_list(request, account, status, limit=None, offset=None, order_by=None):
  """ List all available records for an account.

  This includes records that *account* owns, records that have been fully shared
  with *account*, and records that are shared with *account* via carenets.

  Will return :http:statuscode:`200` with a list of records on success.

  """

  records = account.records_owned_by.all()
  full_shares = account.fullshares_to.all()
  carenet_shares = account.carenetaccount_set.all()
  return render_template('record_list', {'records': records, 'full_shares' : full_shares, 'carenet_shares': carenet_shares})


def record_get_owner(request, record):
  """ Get the owner of a record.

  Will always return :http:statuscode:`200`. The response body will contain the
  owner's email address, or the empty string if the record is unowned.
  
  """

  owner_email = ""
  if record.owner:
    owner_email = record.owner.email
  return render_template('account_id', {'id': owner_email})


def record_set_owner(request, record):
  """ Set the owner of a record.

  request.POST must contain the email address of the new owner.

  Will return :http:statuscode:`200` with information about the new
  owner on success, :http:statuscode:`400` if request.POST is empty
  or the passed email address doesn't correspond to an existing principal.
  
  """

  try:
    record.owner = Principal.objects.get(email=request.raw_post_data)
    record.save()
  except Principal.DoesNotExist:
    logging.error('Post has no owner in body')
    return HttpResponseBadRequest()
  return render_template('account', {'account': record.owner})
    

def record(request, record):
  """ Get information about an individual record.

  Will return :http:statuscode:`200` with information about the record on
  success.

  """

  return render_template('record', {'record': record})


def record_phas(request, record):
  """ List userapps bound to a given record.

  request.GET may optionally contain:

  * *type*: An XML schema namespace. If specified, only apps which
    explicitly declare themselves as supporting that namespace will
    be returned.

  Will return :http:statuscode:`200` with the list of matching apps
  on success.

  """

  phas = record.phas

  # are we filtering by schema?
  type = request.GET.get('type', None)
  if type:
    schema = DocumentSchema.objects.get(type=type)
    phas = [pha for pha in phas if pha.schema == schema]

  # interpolate the the start_url_template into start_url
  for pha in phas:
    pha.start_url = utils.url_interpolate(pha.start_url_template, {'record_id' : record.id})
  
  return render_template('phas', {'phas':phas})


def record_pha(request, record, pha):
  """ Get information about a given userapp bound to a record.

  Will return :http:statuscode:`200` with information about the app on success,
  :http:statuscode:`404` if the app isn't actually bound to the record.

  """

  try:
    pha = record.pha_shares.get(with_pha__email = pha.email).with_pha
  except PHAShare.DoesNotExist:
    raise Http404
  pha.start_url = utils.url_interpolate(pha.start_url_template, {'record_id' : record.id})
  return render_template('pha', {'pha':pha})


def record_notify(request, record):
  """ Send a notification about a record to all accounts authorized to be notified.

  Notifications should be short alerts, as compared to full inbox messages, and
  may only be formatted as plaintext.

  request.POST must contain:

  * *content*: The plaintext content of the notification.

  request.POST may contain:

  * *document_id*: The document to which this notification pertains.

  * *app_url*: A callback url to the app for more information.

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if 
  *content* wasn't passed.

  """

  CONTENT = 'content'
  if request.POST.has_key(CONTENT):
    content = request.POST[CONTENT]
    record.notify(request.principal.effective_principal, 
                  content     = content, 
                  document_id = request.POST.get('document_id', None), 
                  app_url     = request.POST.get('app_url', None))
    # return the notification ID instead of DONE?
    return DONE
  else:
    return HttpResponseBadRequest()


def record_shares(request, record):
  """ List the shares of a record.

  This includes shares with apps (phashares) and full shares with accounts
  (fullshares).
  
  Will return :http:statuscode:`200` with a list of shares on success.

  """

  pha_shares = record.pha_shares.all()
  full_shares = record.fullshares.all()
  return render_template('shares', {'fullshares': full_shares, 'phashares':pha_shares, 'record': record})


def record_share_add(request, record):
  """ Fully share a record with another account.

  A full share gives the recipient account full access to all data and apps 
  on the record, and adds the recipient to the list of accounts who are alerted
  when the record gets a new alert or notification.

  request.POST must contain:

  * *account_id*: the email address of the recipient account.

  request.POST may contain:

  * *role_label*: A label for the share (usually the relationship between the
    record owner and the recipient account, i.e. 'Guardian')

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if
  *account_id* was not passed, and :http:statuscode:`404` if the passed
  *account_id* does not correspond to an existing Account.

  """

  ACCOUNT_ID = 'account_id'
  try:
    if request.POST.has_key(ACCOUNT_ID):
      other_account_id = request.POST[ACCOUNT_ID].lower().strip()
      account = Account.objects.get(email=other_account_id)
      RecordNotificationRoute.objects.get_or_create(account = account, record = record)
      share = AccountFullShare.objects.get_or_create(record = record, with_account = account, role_label = request.POST.get('role_label', None))
      return DONE
    else:
      return HttpResponseBadRequest()
  except Account.DoesNotExist:
    raise Http404
  except Principal.DoesNotExist:
    raise Http404


def record_share_delete(request, record, other_account_id):
  """ Undo a full record share with an account.
  
  Will return :http:statuscode:`200` on success, :http:statuscode:`404` if
  *other_account_id* doesn't correspond to an existing Account.

  """

  try:
    shares = AccountFullShare.objects.filter(record = record, with_account = Account.objects.get(email=other_account_id.lower().strip()))
    shares.delete()
    return DONE
  except Account.DoesNotExist:
    raise Http404
  except Principal.DoesNotExist:
    raise Http404

@transaction.commit_on_success
def record_create(request, principal_email=None, external_id=None):
  """ Create a new record.

  For 1:1 mapping of URLs to views: just calls 
  :py:meth:`~indivo.views.record._record_create`.

  """
  
  return _record_create(request, principal_email, external_id)

@transaction.commit_on_success
def record_create_ext(request, principal_email=None, external_id=None):
  """ Create a new record with an associated external id.

  For 1:1 mapping of URLs to views: just calls 
  :py:meth:`~indivo.views.record._record_create`.

  """

  return _record_create(request, principal_email, external_id)

def _record_create(request, principal_email=None, external_id=None):
  """ Create an Indivo record.

  request.POST must contain raw XML that is a valid Indivo Contact
  document (see :doc:`/schemas/contact-schema`).
  
  This call will create a new record containing the following 
  information:

  * *creator*: Corresponds to ``request.principal``.

  * *label*: The full name of the new record, specified in the
    contact document.

  * *owner*: Corresponds to ``request.principal``.

  * *external_id* An external identifier for the record, if 
    passed in.

  Additionally, this call will create a Contact document for the record.

  Will return :http:statuscode:`200` with information about the record on
  success, :http:statuscode:`400` if the contact data in request.POST was
  empty or invalid XML.
  
  """

  # If the xml data is not valid return an HttpResponseBadRequest Obj
  xml_data = request.raw_post_data
  try:
    etree.XML(xml_data)
  except:
    return HttpResponseBadRequest("Contact XML not valid")

  record_external_id = Record.prepare_external_id(external_id, principal_email)
    
  if external_id:
    record , created_p = Record.objects.get_or_create(
      external_id = record_external_id,
      defaults = {
        'creator' : request.principal,
        'label' : Contacts.from_xml(xml_data).full_name,
        'owner' : request.principal})
  else:
    record = Record.objects.create(
      external_id = record_external_id,
      creator = request.principal,
      label = Contacts.from_xml(xml_data).full_name,
      owner = request.principal)
    created_p = True

  # only set up the new contact document if the record is new
  # otherwise just return the existing record
  if created_p:
    # Create default carenets for this particular record
    record.create_default_carenets()

    # Create the contact document
    # use the same external ID as for the record
    # since those are distinct anyways
    doc_external_id = record_external_id

    doc = _document_create( record      = record,
                            creator     = request.principal,
                            pha         = None,
                            content     = xml_data,
                            external_id = doc_external_id)
      
    # save the contact document as the special contact doc
    record.contact = doc
    record.save()

  return render_template('record', {'record' : record}, type='xml')

@transaction.commit_on_success
def record_pha_setup(request, record, pha):
  """ Bind an app to a record without user authorization.

  This call should be used to set up new records with apps required
  for this instance of Indivo to run (i.e. syncer apps that connect to 
  data sources). It can only be made by admins, since it skips the
  normal app authorization process.

  ``request.POST`` may contain raw content that will be used
  as a setup document for the record.

  Will return :http:statuscode:`200` with a valid access token for the
  app bound to the record on success.
  
  """

  # TODO: eventually, when there are permission restrictions on a PHA, 
  # make sure that any permission restrictions on the current PHA are 
  # transitioned accordingly.

  content = request.raw_post_data

  # if there is a document, create it
  if content:
    # is there already a setup doc
    setup_docs = Document.objects.filter(record=record, pha=pha, external_id='SETUP')
    if len(setup_docs) == 0:
      new_doc = _document_create( record      = record,
                                  creator     = request.principal,
                                  pha         = pha,
                                  content     = content,
                                  external_id = Document.prepare_external_id('SETUP', pha, pha_specific=True, record_specific=True))

  # preauthorize the token.
  from indivo.accesscontrol.oauth_servers import OAUTH_SERVER
  access_token = OAUTH_SERVER.generate_and_preauthorize_access_token(pha, record=record)

  # return the token
  return HttpResponse(access_token.to_string(), mimetype="application/x-www-form-urlencoded")

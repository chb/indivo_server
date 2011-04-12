"""
Indivo Views -- Record
"""

#import libxml2
from lxml import etree

from indivo.lib import utils
from indivo.views.documents.document import _document_create
from base import *

ACTIVE_STATE = 'active'



@marsloader()
def record_list(request, account, status, limit=None, offset=None, order_by=None):
  """
  A list of records available for a given account
  """
  records = account.records_owned_by.all()
  full_shares = account.shares_to.all()
  carenet_shares = account.carenetaccount_set.all()
  return render_template('record_list', {'records': records, 'full_shares' : full_shares, 'carenet_shares': carenet_shares})


def record_get_owner(request, record):
  owner_email = ""
  if record.owner:
    owner_email = record.owner.email
  return render_template('account_id', {'id': owner_email})


def record_set_owner(request, record):
  try:
    record.owner = Principal.objects.get(email=request.raw_post_data)
    record.save()
  except Principal.DoesNotExist:
    logging.error('Post has no owner in body')
    return HttpResponseBadRequest()
  return render_template('account', {'account': record.owner})
    

def record(request, record):
  return render_template('record', {'record': record})


def record_phas(request, record):
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
  try:
    pha = record.shares.get(with_pha__email = pha.email).with_pha
  except Share.DoesNotExist:
    raise Http404
  pha.start_url = utils.url_interpolate(pha.start_url_template, {'record_id' : record.id})
  return render_template('pha', {'pha':pha})


def record_notify(request, record):
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
  """ List the shares of a record"""

  shares = record.shares.all()
  return render_template('shares', {'shares': shares, 'record': record})


def record_share_add(request, record):
  """
  Add a share
  FIXME: add label
  """

  ACCOUNT_ID = 'account_id'
  try:
    if request.POST.has_key(ACCOUNT_ID):
      other_account_id = request.POST[ACCOUNT_ID]
      account = Account.objects.get(email=other_account_id)
      RecordNotificationRoute.objects.get_or_create(account = account, record = record)
      share = Share.objects.get_or_create(record = record, with_account = account, role_label = request.POST.get('role_label', None))
      return DONE
    else:
      return HttpResponseBadRequest()
  except Account.DoesNotExist:
    raise Http404
  except Principal.DoesNotExist:
    raise Http404


def record_share_delete(request, record, other_account_id):
  """Remove a share"""

  try:
    shares = Share.objects.filter(record = record, with_account = Account.objects.get(email=other_account_id))
    shares.delete()
    return DONE
  except Account.DoesNotExist:
    raise Http404
  except Principal.DoesNotExist:
    raise Http404

@transaction.commit_on_success
def record_create(request, principal_email=None, external_id=None):
  """For 1:1 mapping of URLs to views: calls _record_create"""
  return _record_create(request, principal_email, external_id)

@transaction.commit_on_success
def record_create_ext(request, principal_email=None, external_id=None):
  """For 1:1 mapping of URLs to views: calls _record_create"""
  return _record_create(request, principal_email, external_id)

def _record_create(request, principal_email=None, external_id=None):
  """
  Create an Indivo record
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


def record_password_reset(request, record):
  # look up the associated user
  pass


@transaction.commit_on_success
def record_pha_setup(request, record, pha):
  """Set up a PHA in a record ahead of time

  FIXME: eventually, when there are permission restrictions on a PHA, make sure that
  any permission restrictions on the current PHA are transitioned accordingly
  """

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
  access_token = OAUTH_SERVER.generate_and_preauthorize_access_token(pha, record=record)

  # return the token
  return HttpResponse(access_token.to_string(), mimetype="application/x-www-form-urlencoded")

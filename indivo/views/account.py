"""
Indivo views for Account
"""

from base import *
import urllib
from indivo.lib import utils
from django.http import HttpResponseBadRequest
from django.db import IntegrityError

ACTIVE_STATE, UNINITIALIZED_STATE = 'active', 'uninitialized'
HTTP_METHOD_GET = 'GET'

def get_id(request):
  principal = request.principal
  
  if principal:
    id = principal.email
  else:
    id = ""
  return render_template('account_id', {'id': id})


def account_password_change(request, account):
  OLD = 'old'
  NEW = 'new'
  if request.POST.has_key(OLD) and request.POST.has_key(NEW):
    if account and account.password_check(request.POST[OLD]):
      account.password = request.POST[NEW]
      account.save()
      return DONE
    else:
      raise PermissionDenied()
  return HttpResponseBadRequest()


def account_reset(request, account):
  account.reset()
  return DONE


def account_set_state(request, account):
  """
  set the state of the account (active/disabled/retired)
  """
  try:
    account.set_state(request.POST['state'])
  except Exception, e:
    raise PermissionDenied(e)
  account.save()
  return DONE


def account_password_set(request, account):
  if account and request.POST.has_key('password'):
    account.password = request.POST['password']
    account.save()
    return DONE
  return HttpResponseBadRequest()


def account_username_set(request, account):
  if account and request.POST.has_key('username'):
    account.set_username(request.POST['username'])
    return DONE
  return HttpResponseBadRequest()


def account_info_set(request, account):
  account.contact_email = request.POST['contact_email']
  account.full_name = request.POST['full_name']
  account.save()
  return DONE


@transaction.commit_on_success
def account_initialize(request, account, primary_secret):
  SECONDARY_SECRET = 'secondary_secret'

  # check primary secret
  if account.primary_secret != primary_secret:
    account.on_failed_login()
    raise PermissionDenied()

  if account.state != UNINITIALIZED_STATE:
    raise PermissionDenied()
  
  # if there is a secondary secret in the account, check it in the form
  if request.POST.has_key(SECONDARY_SECRET):
    secondary_secret = request.POST[SECONDARY_SECRET]
    if account.secondary_secret and secondary_secret != account.secondary_secret:
      account.on_failed_login()
      raise PermissionDenied()

    account.state = ACTIVE_STATE
    account.send_welcome_email()
    account.save()

    return DONE
  return HttpResponseBadRequest()


def account_primary_secret(request, account):
  return render_template('secret', {'secret':account.primary_secret})


def account_info(request, account):
  # get the account auth systems
  auth_systems = account.auth_systems.all()
  return render_template('account', { 'account'       : account,
                                      'auth_systems'  : auth_systems })


def account_check_secrets(request, account, primary_secret):
  SECONDARY_SECRET = 'secondary_secret'

  # check primary secret
  if account.primary_secret != primary_secret:
    account.on_failed_login()
    raise PermissionDenied()

  # if there is a secondary secret in the account, check it in the form
  if request.GET.has_key(SECONDARY_SECRET):
    secondary_secret = request.GET[SECONDARY_SECRET]
    if account.secondary_secret and secondary_secret != account.secondary_secret:
      raise PermissionDenied()
  return DONE

def account_search(request):
  """Search accounts"""

  fullname      = request.GET.get('fullname', None)
  contact_email = request.GET.get('contact_email', None)

  if not (fullname or contact_email):
    raise Exception("At least one criteria needed")

  query = Account.objects
  if fullname:
    query = query.filter(full_name = fullname)
  if contact_email:
    query = query.filter(contact_email = contact_email)

  return render_template('accounts_search', {'accounts': query}, type='xml')


@transaction.commit_manually
def account_authsystem_add(request, account):
  USERNAME, PASSWORD = 'username', 'password'

  if request.POST.has_key(USERNAME):
    username = request.POST[USERNAME]
  else:
    transaction.rollback()
    return HttpResponseBadRequest('No username')

  try:
    system = AuthSystem.objects.get(short_name = request.POST['system'])
    account.auth_systems.create(username    = username.lower().strip(), 
                                auth_system = system)
  except AuthSystem.DoesNotExist:
    transaction.rollback()
    raise PermissionDenied()
  except IntegrityError:
    transaction.rollback()
    return HttpResponseBadRequest('Duplicate attempt to add authsystem to account')
  else:
    if system == AuthSystem.PASSWORD() and request.POST.has_key(PASSWORD):
      account.password_set(request.POST[PASSWORD])
      account.set_state(ACTIVE_STATE)
      account.save()
    
    transaction.commit()
    # return the account info instead
    return DONE


def account_forgot_password(request):
  contact_email = request.GET.get('contact_email', None)
  if contact_email:
    try:
      account = Account.objects.get(contact_email = contact_email)
    except Account.DoesNotExist:
      raise PermissionDenied()
    except:
      raise PermissionDenied()
  if account.state != UNINITIALIZED_STATE:
    account.reset()
  else:
    return HttpResponseBadRequest("Account has not been initialized")
  account.send_forgot_password_email()
  return HttpResponse("<secret>%s</secret>" % account.secondary_secret)


def account_resend_secret(request, account):
  # FIXME: eventually check the status of the account
  account.send_secret()
  
  # probably ok to return DONE, but it should just be empty, like Flickr
  return DONE
  

def account_secret(request, account):
  return HttpResponse("<secret>%s</secret>" % account.secondary_secret)

@transaction.commit_on_success
def account_create(request):
  """Create an account"""

  account_id = request.POST.get('account_id', None)
  if not account_id or not utils.is_valid_email(account_id):
    return HttpResponseBadRequest("Account ID not valid")

  new_account, create_p = Account.objects.get_or_create(email=urllib.unquote(account_id))
  if create_p:
    """
    generate a secondary secret or not? Requestor can say no.
    trust model makes sense: the admin app requestor only decides whether or not 
    they control the additional interaction or if it's not necessary. They never
    see the primary secret.
    """

    new_account.full_name = request.POST.get('full_name', '')
    new_account.contact_email = request.POST.get('contact_email', account_id)

    new_account.creator = request.principal

    password            = request.POST.get('password', None)
    primary_secret_p    = (request.POST.get('primary_secret_p', "0") == "1")
    secondary_secret_p  = (request.POST.get('secondary_secret_p', "0") == "1")

    # we don't allow setting the password here anymore

    new_account.save()

    #SZ: if password and len(password) > 0:
    if primary_secret_p:
      new_account.generate_secrets(secondary_secret_p = secondary_secret_p)
      new_account.send_secret()

  return render_template('account', {'account' : new_account}, type='xml')

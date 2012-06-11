""" 
.. module:: views.account
   :synopsis: Account-related Indivo view implementations.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from base import *
import urllib
import logging
from indivo.lib import utils
from indivo.lib.sample_data import IndivoDataLoader
from django.http import HttpResponseBadRequest
from django.db import IntegrityError
from django.conf import settings
from django.db.models import Q
from oauth.oauth import HTTPRequest, OAuthRequest

ACTIVE_STATE, UNINITIALIZED_STATE = 'active', 'uninitialized'

def account_password_change(request, account):
    """ Change a account's password.

    request.POST must contain:
    
    * *old*: The existing account password.
    * *new*: The desired new password.

    Will return :http:statuscode:`200` on success,
    :http:statuscode:`403` if the old password didn't
    validate, :http:statuscode:`400` if the POST data
    didn't contain both an old password and a new one.
    
    """

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
    """ Reset an account to an ``uninitialized`` state.

    Just calls into :py:meth:`~indivo.models.accounts.Account.reset`.

    Will return :http:statuscode:`200` on success.

    """

    account.reset()
    return DONE


def account_set_state(request, account):
    """ Set the state of an account. 
    
    request.POST must contain:
    
    * *state*: The desired new state of the account.
    
    Options are: 
    
    * ``active``: The account is ready for use.
    
    * ``disabled``: The account has been disabled,
      and cannot be logged into.
      
    * ``retired``: The account has been permanently
      disabled, and will never allow login again.
      Retired accounts cannot be set to any other 
      state.
    
    Will return :http:statuscode:`200` on success,
    :http:statuscode:`403` if the account has been
    retired and :http:statuscode:`400` if POST data
    did not contain a "status" parameter
    
    """
    
    if not request.POST.get('state'):
        return HttpResponseBadRequest('No state')
    
    try:
        account.set_state(request.POST['state'])
    except Exception, e:
        raise PermissionDenied(e)
    account.save()
    return DONE


def account_password_set(request, account):
    """ Force the password of an account to a given value.

    This differs from 
    :py:meth:`~indivo.views.account.account_password_change`
    in that it does not require validation of the old password. This
    function is therefore admin-facing, whereas 
    :py:meth:`~indivo.views.account.account_password_change` 
    is user-facing.

    request.POST must contain:
    
    * *password*: The new password to set.

    Will return :http:statuscode:`200` on success, :http:statuscode:`400`
    if the passed POST data didn't contain a new password.

    """

    if account and request.POST.has_key('password'):
        account.password = request.POST['password']
        account.save()
        return DONE
    return HttpResponseBadRequest()


def account_username_set(request, account):
    """ Force the username of an account to a given value.

    request.POST must contain:

    * *username*: The new username to set.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`400` if the POST data doesn't conatain
    a new username.

    """

    if account and request.POST.has_key('username'):
        account.set_username(request.POST['username'])
        return DONE
    return HttpResponseBadRequest()


def account_info_set(request, account):
    """ Set basic information about an account.
    
    request.POST can contain any of:
    
    * *contact_email*: A new contact email for the account.
    
    * *full_name*: A new full name for the account.
    
    Each passed parameter will be updated for the account.
    
    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`400` if the POST data contains none of
    the settable parameters.
    
    """
    
    contact_email = request.POST.get('contact_email')
    full_name = request.POST.get('full_name')
    if not contact_email and not full_name:
        return HttpResponseBadRequest('No parameter given')
    
    if contact_email:
        account.contact_email = contact_email
    if full_name:
        account.full_name = full_name
    
    account.save()
    return DONE


@transaction.commit_on_success
def account_initialize(request, account, primary_secret):
    """ Initialize an account, activating it.

    After validating primary and secondary secrets, changes the 
    account's state from ``uninitialized`` to ``active`` and sends
    a welcome email to the user.

    If the account has an associated secondary secret, request.POST 
    must contain:

    * *secondary_secret*: The secondary_secret generated for the account.

    Will return :http:statuscode:`200` on success, :http:statuscode:`403`
    if the account has already been initialized or if either of the account
    secrets didn't validate, and :http:statuscode:`400` if a secondary secret
    was required, but didn't appear in the POST data.
    
    """
    
    SECONDARY_SECRET = 'secondary_secret'
    
    # check primary secret
    if account.primary_secret != primary_secret:
        account.on_failed_login()
        raise PermissionDenied()
    
    if account.state != UNINITIALIZED_STATE:
        raise PermissionDenied()
    
    # if there is a secondary secret in the account, check it in the form
    if not account.secondary_secret or request.POST.has_key(SECONDARY_SECRET):
        secondary_secret = request.POST.get(SECONDARY_SECRET)
        if account.secondary_secret and secondary_secret != account.secondary_secret:
            account.on_failed_login()
            raise PermissionDenied()
        
        account.state = ACTIVE_STATE
        try:
            account.send_welcome_email()
        except Exception, e:
            logging.exception(e)
        account.save()
        
        return DONE
    return HttpResponseBadRequest()


def account_primary_secret(request, account):
    """ Display an account's primary secret.

    This is an admin-facing call, and should be used sparingly,
    as we would like to avoid sending primary-secrets over the
    wire. If possible, use 
    :py:meth:`~indivo.views.account.account_check_secrets`
    instead.

    Will return :http:statuscode:`200` with the primary secret on success.
    
    """

    return render_template('secret', {'secret': account.primary_secret})


def account_info(request, account):
    """ Display information about an account.

    Return information includes the account's secondary-secret,
    full name, contact email, login counts, state, and auth 
    systems.

    Will return :http:statuscode:`200` on success, with account info
    XML.

    """
    # get the account auth systems
    auth_systems = account.auth_systems.all()
    return render_template('account', {'account': account,
                                'auth_systems': auth_systems})


def account_check_secrets(request, account, primary_secret):
    """ Validate an account's primary and secondary secrets.

    If the secondary secret is to be validated, request.GET must
    contain:

    * *secondary_secret*: The account's secondary secret.

    This call will validate the prmary secret, and the secondary
    secret if passed.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`403` if either validation fails.

    """

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
    """ Search for accounts by name or email.
    
    request.GET must contain the query parameters, any of:
    
    * *fullname*: The full name of the account
    
    * *contact_email*: The contact email for the account.
    
    This call returns all accounts matching any part of any of the
    passed query parameters: i.e. it ORs together the query parameters 
    and runs a partial-text match on each.
    
    Will return :http:statuscode:`200` with XML describing
    matching accounts on success, :http:statuscode:`400` if
    no query parameters are passed.
    
    """
    
    fullname      = request.GET.get('fullname', None)
    contact_email = request.GET.get('contact_email', None)
    
    if not (fullname or contact_email):
        return HttpResponseBadRequest('No search criteria given')
    
    query_filter = Q()
    if fullname:
        query_filter |= Q(full_name__icontains = fullname)
    if contact_email:
        query_filter |= Q(contact_email__icontains = contact_email)

    query = Account.objects.filter(query_filter)
    
    return render_template('accounts_search', {'accounts': query}, type='xml')


@transaction.commit_manually
def account_authsystem_add(request, account):
    """ Add a new method of authentication to an account.

    Accounts cannot be logged into unless there exists a
    mechanism for authenticating them. Indivo supports one
    built-in mechanism, password auth, but is extensible with
    other mechanisms (i.e., LDAP, etc.). If an external mechanism 
    is used, a UI app is responsible for user authentication, and 
    this call merely registers with indivo server the fact that 
    the UI can handle auth. If password auth is used, this call 
    additionally registers the password with indivo server.
    Thus, this call can be used to add internal or external auth 
    systems.

    request.POST must contain:

    * *system*: The identifier (a short slug) associated with the
      desired auth system. ``password`` identifies the internal
      password system, and external auth systems will define their
      own identifiers.

    * *username*: The username that this account will use to 
      authenticate against the new authsystem
      
    * *password*: The password to pair with the username.
      **ONLY REQUIRED IF THE AUTH SYSTEM IS THE INTERNAL
      PASSWORD SYSTEM**.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`403` if the indicated auth system doesn't exist,
    and :http:statuscode:`400` if the POST data didn't contain a system
    and a username (and a password if system was ``password``), or if
    the account is already registered for the given authsystem, or a 
    different account is already registered for the given authsystem with
    the same username.

    """
    
    # check for username
    USERNAME, PASSWORD = 'username', 'password'
    
    if request.POST.has_key(USERNAME):
        username = request.POST[USERNAME]
    else:
        transaction.rollback()
        return HttpResponseBadRequest('No username')
    
    # did we get a system?
    desired_system = request.POST.get('system')
    if not desired_system:
        transaction.rollback()
        return HttpResponseBadRequest('No system')
    
    # if we got "password" as system, did we get a password?
    new_password = None
    if 'password' == desired_system:
        new_password = request.POST.get(PASSWORD)
        if not new_password:
            transaction.rollback()
            return HttpResponseBadRequest('No password')
    
    # set the auth system
    try:
        system = AuthSystem.objects.get(short_name = desired_system)
        account.auth_systems.create(username = username, 
                                 auth_system = system)
    except AuthSystem.DoesNotExist:
        transaction.rollback()
        raise PermissionDenied()
    except IntegrityError:
        transaction.rollback()
        return HttpResponseBadRequest('Duplicate attempt to add authsystem to account')
    else:
        if system == AuthSystem.PASSWORD() and new_password:
            account.password_set(new_password)
            account.set_state(ACTIVE_STATE)
            account.save()
        
        transaction.commit()
        # return the account info instead
        return DONE


def account_forgot_password(request, account):
    """ Resets an account if the user has forgotten its password.

    This is a convenience call which encapsulates
    :py:meth:`~indivo.views.account.account_reset`, 
    :py:meth:`~indivo.views.account.account_resend_secret`, and
    :py:meth:`~indivo.views.account.account_secret`. In summary,
    it resets the account to an uninitialized state, emails
    the user with a new primary-secret, and returns the
    secondary secret for display.

    Will return :http:statuscode:`200` with the secondary secret
    on success, :http:statuscode:`400` if the account hasn't yet
    been initialized and couldn't possibly need a reset. If the
    account has no associated secondary secret, the return XML
    will be empty.
    
    """

    if account.state != UNINITIALIZED_STATE:
        account.reset()
    else:
        return HttpResponseBadRequest("Account has not been initialized")
    
    try:
        account.send_forgot_password_email()
    except Exception, e:
        logging.exception(e)
    return HttpResponse("<secret>%s</secret>" % account.secondary_secret)


def account_resend_secret(request, account):
    """ Sends an account user their primary secret in case they lost it.

    Will return :http:statuscode:`200` on success.

    """

    # FIXME: eventually check the status of the account
    try:
        account.send_secret()
    except Exception, e:
        logging.exception(e)
    
    # probably ok to return DONE, but it should just be empty, like Flickr
    return DONE


def account_secret(request, account):
    """ Return the secondary secret of an account.

    Will always return :http:statuscode:`200`. If the account 
    has no associated secondary secret, the return XML will
    be empty.

    """

    return HttpResponse("<secret>%s</secret>" % account.secondary_secret)

@transaction.commit_on_success
def account_create(request):
    """ Create a new account, and send out initialization emails.
    
    ``request.POST`` holds the creation arguments. 

    In Demo Mode, this call
    automatically creates new records for the account, populated with
    sample data. See :doc:`/sample-data` for details.
    
    Required Parameters:
    
    * *account_id*: an identifier for the new address. Must be formatted
      as an email address.
    
    Optional Parameters:
    
    * *full_name*: The full name to associate with the account. Defaults
      to the empty string.
    
    * *contact_email*: A valid email at which the account holder can 
      be reached. Defaults to the *account_id* parameter.
    
    * *primary_secret_p*: ``0`` or ``1``. Whether or not to associate 
      a primary secret with the account. Defaults to ``1``.
    
    * *secondary_secret_p*: ``0`` or ``1``. Whether or not to associate
      a secondary secret with the account. Defaults to ``0``.
    
    After creating the new account, this call generates secrets for it,
    and then emails the user (at *contact_email*) with their activation
    link, which contains the primary secret.
    
    This call will return :http:statuscode:`200` with info about the new
    account on success, :http:statuscode:`400` if *account_id* isn't 
    provided or isn't a valid email address, or if an account already
    exists with an id matching *account_id*.
      
    """
    
    account_id = request.POST.get('account_id', None)
    if not account_id or not utils.is_valid_email(account_id):
        return HttpResponseBadRequest("Account ID not valid")
    
    contact_email = request.POST.get('contact_email', account_id)
    if not contact_email or not utils.is_valid_email(contact_email):
        return HttpResponseBadRequest("Contact email not valid")
    
    new_account, create_p = Account.objects.get_or_create(email=urllib.unquote(account_id).lower().strip())
    if create_p:
        
        # generate a secondary secret or not? Requestor can say no.
        # trust model makes sense: the admin app requestor only decides whether or not 
        # they control the additional interaction or if it's not necessary. They never
        # see the primary secret.
        
        new_account.full_name = request.POST.get('full_name', '')
        new_account.contact_email = contact_email
        
        new_account.creator = request.principal
        
        password            = request.POST.get('password', None)
        primary_secret_p    = (request.POST.get('primary_secret_p', "1") == "1")
        secondary_secret_p  = (request.POST.get('secondary_secret_p', "0") == "1")
        
        # we don't allow setting the password here anymore
        new_account.save()
            
        if settings.DEMO_MODE:
            loader = IndivoDataLoader(request.principal)
            
            # Create new records for the account, populated by sample data.
            for record_label, data_profile in settings.DEMO_PROFILES.iteritems():
                
                # Create the record
                record = Record.objects.create(creator=request.principal,
                                               label=record_label,
                                               owner=new_account)

                try:
                    # Load the data: no transactions, as we're already managing them above
                    loader.load_profile(record, data_profile, transaction=False)
                except Exception, e: # Something went wrong: roll everything back and fail
                    logging.exception(e)
                    raise

        if primary_secret_p:
            new_account.generate_secrets(secondary_secret_p = secondary_secret_p)
            try:
                new_account.send_secret()
            except Exception, e:
                logging.exception(e)

                
    # account already existed
    else:
        return HttpResponseBadRequest("An account with email address %s already exists." % account_id)
    
    return render_template('account', {'account': new_account}, type='xml')

def get_connect_credentials(request, account, pha):
    """ Get oAuth credentials for an app to run in Connect or SMART REST mode.

    Generates access tokens for *pha* to run against the *record_id* specified in ``request.POST``, authorized by
    *account*. Generates 2 tokens: one for SMART Connect use, and one for SMART REST use.
    
    """

    carenet = record = None
    carenet_id = request.POST.get('carenet_id', None)
    record_id = request.POST.get('record_id', None)

    import pdb;pdb.set_trace()
    if carenet_id:
        try:
            carenet=Carenet.objects.get(id=carenet_id)
        except Carenet.DoesNotExist:
            raise Http404
        except Carenet.MultipleObjectsReturned:
            raise Exception("Multiple carenets with same id--database is corrupt")

    elif record_id:
        try:
            record = Record.objects.get(id=record_id)
        except Record.DoesNotExist:
            raise Http404
        except Record.MultipleObjectsReturned:
            raise Exception("Multiple records with same id--database is corrupt")

    # Generate the tokens
    from indivo.accesscontrol.oauth_servers import OAUTH_SERVER
    rest_token = OAUTH_SERVER.generate_and_preauthorize_access_token(pha, record=record, 
                                                                     carenet=carenet, account=account)
    connect_token = OAUTH_SERVER.generate_and_preauthorize_access_token(pha, record=record, 
                                                                        carenet=carenet, account=account)
    connect_token.connect_auth_p = True
    connect_token.save()

    # Generate a 2-legged oauth header for the rest token, based on the pha's start_url
    url = utils.url_interpolate(pha.start_url_template, {'record_id':record_id or '', 'carenet_id':carenet_id or ''})
    request = HTTPRequest("GET", url, HTTPRequest.FORM_URLENCODED_TYPE, '', {})
    oauth_params = {
        'smart_container_api_base': settings.SITE_URL_PREFIX,
        'smart_oauth_token': rest_token.token,
        'smart_oauth_token_secret': rest_token.token_secret,
        'smart_user_id': account.email,
        'smart_app_id': pha.email,
        'smart_record_id': record_id,
        }
    oauth_request = OAuthRequest(consumer=pha,
                                 token=None, # no access tokens: 2-legged request
                                 http_request=request,
                                 oauth_parameters=oauth_params)
    oauth_request.sign()
    auth_header = oauth_request.to_header()["Authorization"]

    return render_template('connect_credentials', 
                           { 'connect_token': connect_token,
                             'rest_token': rest_token,
                             'api_base': settings.SITE_URL_PREFIX,
                             'oauth_header': auth_header,
                             'app_email':pha.email}, 
                           type='xml')
                                 
USER_PREFS_EXTID = "%s_USER_PREFERENCES"

def get_user_preferences(request, account, pha):
    """ Get app-specific User Preferences for an account.

    We're just storing these as app-specific documents with a specific external ID.
    ID is "{account_id}_USER_PREFERENCES". Note that this will be further prepared
    by :py:meth:`~indivo.models.Document.prepare_external_id` before insertion into
    the database.

    """

    prefs_doc = _get_prefs_doc(account, pha)
    return HttpResponse(prefs_doc.content if prefs_doc else '', mimetype="text/plain")

def set_user_preferences(request, account, pha):
    """ Set app-specific User Preferences for an account.

    Overrides all existing preferences.

    """

    from indivo.views.documents.document import app_document_create_or_update_ext
    return app_document_create_or_update_ext(request, pha, USER_PREFS_EXTID%account.id)

def delete_user_preferences(request, account, pha):
    """ Delete all app-specific User Preferences for an account. """
    prefs_doc = _get_prefs_doc(account, pha)
    if prefs_doc:
        prefs_doc.delete()
    return DONE

def _get_prefs_doc(account, pha):
    from indivo.models import Document
    from indivo.views.documents.document import _get_document
    prepared_id = Document.prepare_external_id(USER_PREFS_EXTID%account.id, pha, pha_specific=True, record_specific=False)
    return _get_document(pha=pha, external_id=prepared_id)

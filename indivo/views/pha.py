"""
.. module:: views.pha
 :synopsis: Indivo view implementations for userapp-related calls.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

import urllib, urlparse
import logging

from base import *

from oauth.djangoutils import extract_request
from oauth import oauth
from indivo.views.documents.document import _get_document
from indivo.lib import iso8601
import base64, hmac, datetime

def all_phas(request):
    """ List all available userapps.

    Will return :http:statuscode:`200` with an XML list of apps on success.

    """

    phas = PHA.objects.all()
    return render_template('phas', {'phas': phas}, type="xml")
    
def pha(request, pha):
    """ Return a description of a single userapp.

    Will return :http:statuscode:`200` with an XML description of the app 
    on success.
    
    """

    return render_template('pha', {'pha' : pha}, type="xml")

def pha_record_delete(request, record, pha):
    """ Remove a userapp from a record.

    This is accomplished by deleting the app from all carenets belonging to
    the record, then removing the Shares between the record and the app.

    Will return :http:statuscode:`200` on success, :http:statuscode:`404` if
    either the record or the app don't exist.

    """

    try:
        # delete all the carenet placements of the app
        CarenetPHA.objects.filter(carenet__record = record, pha=pha).delete()

        # delete all the share objects that matter
        PHAShare.objects.filter(with_pha=pha, record=record.id).delete()
    except:
        raise Http404
    return DONE


def pha_delete(request, pha):
    """ Delete a userapp from Indivo.

    This call removes the app entirely from indivo, so it will never be
    accessible again. To remove an app just from a single record, see
    :py:meth:`~indivo.views.pha.pha_record_delete`.

    Will return :http:statuscode:`200` on success.

    """

    try:
        pha.delete()
    except:
        raise Http404
    return DONE
    
##
## OAuth Process
##

def request_token(request):
    """ Get a new request token, bound to a record or carenet if desired.

    request.POST may contain **EITHER**:

    * *indivo_record_id*: The record to which to bind the request token.
    
    * *indivo_carenet_id*: The carenet to which to bind the request token.

    Will return :http:statuscode:`200` with the request token on success,
    :http:statuscode:`403` if the oauth signature on the request was missing
    or faulty.

    """

    # ask the oauth server to generate a request token given the HTTP request
    try:
        # we already have the oauth_request in context, so we don't get it again
        from indivo.accesscontrol.oauth_servers import OAUTH_SERVER
        request_token = OAUTH_SERVER.generate_request_token(request.oauth_request, 
                                                            record_id = request.POST.get('indivo_record_id', None),
                                                            carenet_id = request.POST.get('indivo_carenet_id', None))
        return HttpResponse(request_token.to_string(), mimetype='text/plain')
    except oauth.OAuthError, e:
        # an exception can be raised if there is a bad signature (or no signature) in the request
        raise PermissionDenied()


def exchange_token(request):
    """ Exchange a request token for a valid access token.

    This call requires that the request be signed with a valid oauth request
    token that has previously been authorized.

    Will return :http:statuscode:`200` with the access token on success,
    :http:statuscode:`403` if the oauth signature is missing or invalid.

    """
    
    # ask the oauth server to exchange a request token into an access token
    # this will check proper oauth for this action

    try:
        from indivo.accesscontrol.oauth_servers import OAUTH_SERVER
        access_token = OAUTH_SERVER.exchange_request_token(request.oauth_request)
        # an exception can be raised if there is a bad signature (or no signature) in the request
    except:
        raise PermissionDenied()
    
    return HttpResponse(access_token.to_string(), mimetype='text/plain')

##
## OAuth internal calls
##

def session_create(request):
    """ Authenticate a user and register a web session for them.

    request.POST must contain:

    * *username*: the username of the user to authenticate.

    request.POST may contain **EITHER**:
    
    * *password*: the password to use with *username* against the
        internal password auth system.

    * *system*: An external auth system to authenticate the user
    
    Will return :http:statuscode:`200` with a valid session token 
    on success, :http:statuscode:`400` if no username was provided, :http:statuscode:`403` if the passed credentials were
    invalid or it the passed *system* doesn't exist.
    
    """

    from indivo.accesscontrol import auth
    user = None
    username = None
    password = None
    if request.POST.has_key('username'):
        username = request.POST['username']
    else:
        return HttpResponseBadRequest('No username provided')
    
    if request.POST.has_key('password'):
        password = request.POST['password']
        user = auth.authenticate(request, username, password)

        if not password and request.POST.has_key('system'):
                system = request.POST['system']
                try:
                        AuthSystem.objects.get(short_name=system)
                        user = auth.authenticate(request, username, None, system)
                except AuthSystem.DoesNotExist:
                        raise PermissionDenied()
    if not password and request.POST.has_key('system'):
        system = request.POST['system']
        try:
            AuthSystem.objects.get(short_name=system)
            user = auth.authenticate(request, username, None, system)
        except AuthSystem.DoesNotExist:
            raise PermissionDenied()

    if not user:
        return HttpResponseBadRequest('Wrong username/password')
    if not user:
        raise PermissionDenied()

    if user.is_active:
            # auth worked, created a session based token
            from indivo.accesscontrol.oauth_servers import SESSION_OAUTH_SERVER
            token = SESSION_OAUTH_SERVER.generate_and_preauthorize_access_token(request.principal, user=user)
    else:
            logging.debug('This user is not active')
            raise PermissionDenied()

    return HttpResponse(str(token), mimetype='text/plain')


def request_token_claim(request, reqtoken):
    """ Claim a request token on behalf of an account.

    After this call, no one but ``request.principal`` will be able to
    approve *reqtoken*.

    Will return :http:statuscode:`200` with the email of the claiming principal
    on success, :http:statuscode:`403` if the token has already been claimed.

    """

    # already claimed by someone other than me?
    if reqtoken.authorized_by != None and reqtoken.authorized_by != request.principal:
        raise PermissionDenied()
    
    reqtoken.authorized_by = request.principal
    reqtoken.save()

    return HttpResponse(request.principal.email)


def request_token_info(request, reqtoken):
    """ Get information about a request token.

    Information includes: 

    * the record/carenet it is bound to
    
    * Whether the bound record/carenet has been authorized before
    
    * Information about the app for which the token was generated.

    Will return :http:statuscode:`200` with the info on success.
    
    """

    share = None

    try:
        if reqtoken.record:
            share = PHAShare.objects.get(record = reqtoken.record, with_pha = reqtoken.pha)
        elif reqtoken.carenet:
            # if there is a carenet, then we look up the corresponding record
            # and see if this app is already granted access to it.
            #
            # note that the user will still need to be in this carenet to approve
            # the request token
            share = PHAShare.objects.get(record = reqtoken.carenet.record, with_pha = reqtoken.pha)
    except PHAShare.DoesNotExist:
        pass

    return render_template('requesttoken', {'request_token':reqtoken, 'share' : share}, type='xml')


def request_token_approve(request, reqtoken):
    """ Indicate a user's consent to bind an app to a record or carenet.

    request.POST must contain **EITHER**:
    
    * *record_id*: The record to bind to.

    * *carenet_id*: The carenet to bind to.

    Will return :http:statuscode:`200` with a redirect url to the app on success,
    :http:statuscode:`403` if *record_id*/*carenet_id* don't match *reqtoken*.

    """

    record_id = request.POST.get('record_id', None)
    carenet_id = request.POST.get('carenet_id', None)
    
    record = None
    if record_id:
        record = Record.objects.get(id = record_id)

    carenet = None
    if carenet_id:
        carenet = Carenet.objects.get(id = carenet_id)

    # if the request token was bound to a record, then it must match
    if reqtoken.record != None and reqtoken.record != record:
        raise PermissionDenied()

    # if the request token was bound to a carenet
    if reqtoken.carenet != None and reqtoken.carenet != carenet:
        raise PermissionDenied()

    # the permission check that the current user is authorized to connect to this record
    # or to this carenet is already done in accesscontrol
    
    # authorize the request token
    from indivo.accesscontrol.oauth_servers import OAUTH_SERVER
    request_token = OAUTH_SERVER.authorize_request_token(reqtoken.token, record = record, carenet = carenet, account = request.principal)

    # where to redirect to + parameters
    redirect_url = request_token.oauth_callback or request_token.pha.callback_url
    redirect_url += "?oauth_token=%s&oauth_verifier=%s" % (request_token.token, request_token.verifier)

    # redirect to the request token's callback, or if null the PHA's default callback
    return HttpResponse(urllib.urlencode({'location': redirect_url}))

##
## PHA app storage: see views/documents/document.py
##

##
## signing URLs
##
def surl_verify(request):
    """ Verify a signed URL.
    
    The URL must contain the following GET parameters:
    
    * *surl_timestamp*: when the url was generated. Must be within the past hour,
        to avoid permitting old surls.

    * *surl_token* The access token used to sign the url.

    * *surl_sig* The computed signature (base-64 encoded sha1) of the url.

    Will always return :http:statuscode:`200`. The response body will be one of:
    
    * ``<result>ok</result>``: The surl was valid.

    * ``<result>old</result>``: The surl was too old.

    * ``<result>mismatch</result>``: The surl's signature was invalid.
    
    """

    OK = HttpResponse("<result>ok</result>", mimetype="application/xml")
    # May want to add more explanation here
    OLD = HttpResponse("<result>old</result>", mimetype="application/xml")
    MISMATCH = HttpResponse("<result>mismatch</result>", mimetype="application/xml")

    url = request.GET['url']
    parsed_url = urlparse.urlparse(url)
    query = urlparse.parse_qs(parsed_url.query)

    # check timestamp (cheapest thing to check, we check it first)
    url_timestamp = iso8601.parse_utc_date(query['surl_timestamp'][0])
    if (datetime.datetime.utcnow() - url_timestamp) > datetime.timedelta(hours=1):
        return OLD
    
    # generate the secret that should be used here
    try:
        token = AccessToken.objects.get(token = query['surl_token'][0])
    except AccessToken.DoesNotExist:
        return MISMATCH

    # compute the surl secret
    # the string conversion on the secret is required because of a python 2.6 bug
    secret = base64.b64encode(hmac.new(str(token.token_secret), "SURL-SECRET", hashlib.sha1).digest())

    # extract the signature
    surl_sig = query['surl_sig'][0]

    # remove the signature from the URL to verify the rest of it
    # technically this means the signature can be inserted in the middle of the URL,
    # but we'll live with that for now, it shouldn't present a problem
    url_without_sig = url.replace('&%s' % urllib.urlencode({'surl_sig': surl_sig}), '')

    expected_signature = base64.b64encode(hmac.new(secret, url_without_sig, hashlib.sha1).digest())
    
    if expected_signature == surl_sig:
        return OK
    else:
        return MISMATCH

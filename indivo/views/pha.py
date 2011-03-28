"""
Indivo views -- PHAs
"""

import urllib, urlparse

from base import *

from indivo.accesscontrol.oauth_servers import OAUTH_SERVER, SESSION_OAUTH_SERVER
from oauth.djangoutils import extract_request
from oauth import oauth
from indivo.views.documents.document import _get_document
from indivo.accesscontrol import auth
from indivo.lib import iso8601
import base64, hmac, datetime

def all_phas(request):
  """A list of the PHAs as JSON"""

  phas = PHA.objects.all()
  return render_template('phas', {'phas': phas}, type="xml")
  
def pha(request, pha):
  return render_template('pha', {'pha' : pha}, type="xml")

def pha_record_delete(request, record, pha):
  try:
    # delete all the carenet placements of the app
    CarenetPHA.objects.filter(carenet__record = record, pha=pha).delete()

    # delete all the share objects that matter
    Share.objects.filter(with_pha=pha, record=record.id).delete()
  except:
    raise Http404
  return DONE


def pha_delete(request, pha):
  try:
    pha.delete()
  except:
    raise Http404
  return DONE
  
##
## OAuth Process
##

def request_token(request):
    """
    the request-token request URL
    """
    # ask the oauth server to generate a request token given the HTTP request
    try:
      # we already have the oauth_request in context, so we don't get it again
      request_token = OAUTH_SERVER.generate_request_token(request.oauth_request, 
                                                          record_id = request.POST.get('indivo_record_id', None),
                                                          carenet_id = request.POST.get('indivo_carenet_id', None))
      return HttpResponse(request_token.to_string(), mimetype='text/plain')
    except oauth.OAuthError, e:
      # an exception can be raised if there is a bad signature (or no signature) in the request
      raise PermissionDenied()


def exchange_token(request):
    # ask the oauth server to exchange a request token into an access token
    # this will check proper oauth for this action

    try:
      access_token = OAUTH_SERVER.exchange_request_token(request.oauth_request)
      # an exception can be raised if there is a bad signature (or no signature) in the request
    except:
      raise PermissionDenied()

    return HttpResponse(access_token.to_string(), mimetype='text/plain')

def user_authorization(request):
  """Authorize a request token, binding it to a single record.

  A request token *must* be bound to a record before it is approved.
  """

  try:
    token = ReqToken.objects.get(token = request.REQUEST['oauth_token'])
  except ReqToken.DoesNotExist:
    raise Http404

  # are we processing the form
  # OR, is this app already authorized
  if request.method == "POST" or (token.record and token.record.has_pha(token.pha)):
    # get the record from the token
    record = token.record

    # are we dealing with a record already
    if not (record and record.has_pha(token.pha)):
      record = Record.objects.get(id = request.POST['record_id'])
    
      # allowed to administer the record? Needed if the record doesn't have the PHA yet
      if not record.can_admin(request.principal):
        raise Exception("cannot administer this record")

    request_token = OAUTH_SERVER.authorize_request_token(token.token, record = record, account = request.principal)

    # where to redirect to + parameters
    redirect_url = request_token.oauth_callback or request_token.pha.callback_url
    redirect_url += "?oauth_token=%s&oauth_verifier=%s" % (request_token.token, request_token.verifier)

    # redirect to the request token's callback, or if null the PHA's default callback
    return HttpResponseRedirect(redirect_url)
  else:
    records = request.principal.records_administered.all()
    return render_template('authorize', {'token' : token, 'records': records})

##
## OAuth internal calls
##

def session_create(request):
  password = None
  if request.POST.has_key('username'):
    username = request.POST['username']
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

  if not user:
    raise PermissionDenied()

  if user.is_active:
    # auth worked, created a session based token
    token = SESSION_OAUTH_SERVER.generate_and_preauthorize_access_token(request.principal, user=user)
  else:
    raise PermissionDenied()

  return HttpResponse(str(token), mimetype='text/plain')


def request_token_claim(request, reqtoken):
  # already claimed by someone other than me?
  if reqtoken.authorized_by != None and reqtoken.authorized_by != request.principal:
    raise PermissionDenied()
  
  reqtoken.authorized_by = request.principal
  reqtoken.save()

  return HttpResponse(request.principal.email)


def request_token_info(request, reqtoken):
  """
  get info about the request token
  """
  share = None

  try:
    if reqtoken.record:
      share = Share.objects.get(record = reqtoken.record, with_pha = reqtoken.pha)
    elif reqtoken.carenet:
      # if there is a carenet, then we look up the corresponding record
      # and see if this app is already granted access to it.
      #
      # note that the user will still need to be in this carenet to approve
      # the request token
      share = Share.objects.get(record = reqtoken.carenet.record, with_pha = reqtoken.pha)
  except Share.DoesNotExist:
    pass

  return render_template('requesttoken', {'request_token':reqtoken, 'share' : share}, type='xml')


def request_token_approve(request, reqtoken):
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
  request_token = OAUTH_SERVER.authorize_request_token(reqtoken.token, record = record, carenet = carenet, account = request.principal)

  # where to redirect to + parameters
  redirect_url = request_token.oauth_callback or request_token.pha.callback_url
  redirect_url += "?oauth_token=%s&oauth_verifier=%s" % (request_token.token, request_token.verifier)

  # redirect to the request token's callback, or if null the PHA's default callback
  return HttpResponse(urllib.urlencode({'location': redirect_url}))

def get_long_lived_token(request):
  # FIXME: deprecate this for now
  raise PermissionDenied

  if request.method != "POST":
    # FIXME probably 405
    raise Http404
  
  # check if current principal is capable of generating a long-lived token
  # may move this to accesscontrol, but this is a bit of an odd call
  principal = request.principal

  if not principal.share.offline:
    raise PermissionDenied

  new_token, new_secret = oauth.generate_token_and_secret()
  long_lived_token = principal.share.new_access_token(new_token, new_secret, account = None)
  
  return HttpResponse(long_lived_token.to_string(), mimetype='text/plain')  

##
## PHA app storage
##

def app_document_update(request, pha, document_id):
  """for 1:1 mapping from URLs to views. Calls pha_document_update"""
  return pha_document_update(request, pha, document_id)

def record_app_document_update(request, pha, document_id, record):
  """for 1:1 mapping from URLs to views. Calls pha_document_update"""
  return pha_document_update(request, pha, document_id, record=record)

def pha_document_update(request, pha, document_id, record=None):
  try:
    doc = _get_document(record=record, pha=pha, document_id=document_id)
  except Document.DoesNotExist:
    raise Http404

  doc.content = request.raw_post_data
  doc.save()

  return render_template('document', {'doc': doc, 'pha': pha, 'record' :record}, type="xml")

# pha_document replaced by document

# pha_document_meta replaced by document_meta

# pha_document_meta_update replaced by document_meta_update

# pha_document_label replaced by document_label


##
## signing URLs
##
def surl_verify(request):
  """Verifies a signed URL
  
  The URL should contain a bunch of GET parameters, including
  - surl_timestamp
  - surl_token
  - surl_sig
  which are used to verify the rest of the URL
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

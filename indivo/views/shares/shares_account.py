"""
.. module:: views.sharing.shares_account
   :synopsis: Indivo view implementations related to sharing with accounts.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied

def carenet_account_create(request, carenet):
  """ Add an account to a carenet.
  
  request.POST must contain:
  
  * *account_id*: The email of the account to share with.

  * *write*: Whether or not the account can write to the 
    carenet. Can be ``'true'`` or ``'false'``. This is currently
    unused, as carenets are read-only, however it must be provided
    anyways.

  Will return :http:statuscode:`200` on success, :http:statuscode:`404`
  if the specified *account_id* doesn't exist, or :http:statuscode:`400`
  if either *account_id* or *write* is not in request.POST.

  """

  ACCOUNT_ID = 'account_id'
  if request.POST.has_key(ACCOUNT_ID) and \
      request.POST.has_key('write'):
    account_id = request.POST[ACCOUNT_ID].lower().strip()
    try:
      carenets = CarenetAccount.objects.create(
                    carenet = carenet,
                    account = Account.objects.get(email=account_id),
                    can_write = (request.POST['write'] == 'true')
                  )
    except Carenet.DoesNotExist:
      raise Http404
    except Account.DoesNotExist:
      raise Http404
  else:
    return HttpResponseBadRequest()
  return DONE


def carenet_account_list(request, carenet):
  """ List the accounts in a carenet.
  
  Will return :http:statuscode:`200` with a list of accounts on success.

  """

  carenet_accounts = CarenetAccount.objects.select_related().filter(carenet=carenet)

  return render_template('carenet_accounts', {'carenet_accounts' : carenet_accounts}, type="xml")


def carenet_account_delete(request, account, carenet):
  """ Remove an account from a carenet.
  
  Will return :http:statuscode:`200` on success.

  """

  try:
    CarenetAccount.objects.get(
                    account=account, 
                    carenet=carenet).delete()
    return DONE
  except Carenet.DoesNotExist:
    raise Http404
  except Account.DoesNotExist:
    raise Http404


def carenet_account_permissions(request, carenet, account):
  """ List the permissions of an account within a carenet.
  
  Currently, carenets are read-only and accounts can access
  all documents within a carenet, so this call returns static
  XML indicating blanket access.

  Will return :http:statuscode:`200` with the static XML on success.

  """

  # For now, using a static template 
  # since an account has access to all documents within a carenet
  return render_template('permissions', {}, type="xml")


def account_permissions(request, account):
  """ List the carenets that an account has access to.
  
  Will return :http:statuscode:`200` with a list of carenets on success.

  """

  # Since we want to preserve uniqueness we map the carenet accounts list to a dict
  carenets = {}
  map(carenets.__setitem__, 
      [cna.carenet for cna in CarenetAccount.objects.select_related().filter(
        account = account)], [])
  map(carenets.__setitem__,
      [cn for cn in Carenet.objects.select_related().filter(record__owner = account)], [])
  return render_template('carenets', { 'carenets'  : carenets.keys(), 
                                       'record'    : None}, type="xml")

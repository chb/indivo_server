"""
Indivo views -- Sharing
"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied



def carenet_account_create(request, carenet):
  """Link an account to a given carenet
  write=false or write=true"""

  ACCOUNT_ID = 'account_id'
  if request.POST.has_key(ACCOUNT_ID) and \
      request.POST.has_key('write'):
    account_id = request.POST[ACCOUNT_ID]
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
  """List the accounts of a given carenet"""

  carenet_accounts = CarenetAccount.objects.select_related().filter(carenet=carenet)

  return render_template('carenet_accounts', {'carenet_accounts' : carenet_accounts}, type="xml")


def carenet_account_delete(request, account, carenet):
  """Unlink an account from a given carenet"""

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
  """Retrieve the permissions of a given account within a given carenet"""

  # For now, using a static template 
  # since an account has access to all documents within a carenet
  return render_template('permissions', {}, type="xml")


def account_permissions(request, account):
  """Retrieve the permissions of a given account across all carenets"""

  # Since we want to preserve uniqueness we map the carenet accounts list to a dict
  carenets = {}
  map(carenets.__setitem__, 
      [cna.carenet for cna in CarenetAccount.objects.select_related().filter(
        account = account)], [])
  map(carenets.__setitem__,
      [cn for cn in Carenet.objects.select_related().filter(record__owner = account)], [])
  return render_template('carenets', { 'carenets'  : carenets.keys(), 
                                       'record'    : None}, type="xml")

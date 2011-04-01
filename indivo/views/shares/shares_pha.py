"""
Indivo views -- Sharing
"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def carenet_apps_list(request, carenet):
  """List Apps within a given carenet"""
  phas = [cnl.pha for cnl in CarenetPHA.objects.select_related().filter(
                    carenet=carenet 
                  ) 
                  if cnl.pha is not None ]
  return render_template('phas', {'phas' : phas}, type="xml")


def carenet_apps_create(request, carenet, pha):
  """
  Add app to a given carenet
  read/write ability is determined by the user who uses the app, not by the app itself.
  """
  # make sure the PHA already has access to record
  try:
    pha = carenet.record.pha_shares.get(with_pha__email = pha.email).with_pha
  except PHAShare.DoesNotExist:
    raise Http404

  CarenetPHA.objects.get_or_create(carenet=carenet, pha=pha)
  return DONE


def carenet_apps_delete(request, carenet, pha):
  """
  Add app to a given carenet
  read/write ability is determined by the user who uses the app, not by the app itself.
  """

  try:
    carenet_pha = CarenetPHA.objects.get(carenet=carenet, pha__email=pha.email)
    carenet_pha.delete()
  except CarenetPHA.DoesNotExist:
    pass

  return DONE



def carenet_app_permissions(request, carenet, pha):
  """Retrieve the permissions for an app within a carenet"""

  # Not yet implemented
  return DONE

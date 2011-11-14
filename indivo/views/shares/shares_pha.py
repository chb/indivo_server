"""
.. module:: views.sharing.shares_pha
   :synopsis: Indivo view implementations related to sharing applications

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def carenet_apps_list(request, carenet):
  """ List Apps within a given carenet.

  Will return :http:statuscode:`200` with a list of apps on success.
  
  """
  
  phas = [cnl.pha for cnl in CarenetPHA.objects.select_related().filter(
                    carenet=carenet 
                  ) 
                  if cnl.pha is not None ]
  return render_template('phas', {'phas' : phas}, type="xml")


def carenet_apps_create(request, carenet, pha):
  """ Add an app to a carenet

  Read/write capability is determined by the user who uses the app, 
  not by the app itself, so no permissions are assigned here.

  Apps can only be added to carenets if they have already been shared with
  the carenet's record (i.e. the user has agreed to use the app).
 
  Autonomous apps cannot be added to carenets, as they require a full-record
  scope.

  Will return :http:statuscode:`200` on success, :http:statuscode:`404` if 
  there is no existing share between *pha* and *carenet's* record, or
  :http:statuscode:`400` if *pha* is autonomous.

  """
  
  # make sure the PHA already has access to record
  try:
    pha = carenet.record.pha_shares.get(with_pha__email = pha.email).with_pha
  except PHAShare.DoesNotExist:
    raise Http404

  if not pha.is_autonomous:
    CarenetPHA.objects.get_or_create(carenet=carenet, pha=pha)
  else:
    return HttpResponseBadRequest('Autonomous apps may not be linked to individual carenets: they always access the entire record')

  return DONE


def carenet_apps_delete(request, carenet, pha):
  """ Remove an app from a given carenet.

  Will return :http:statuscode:`200` on success, or if *pha* was never in
  *carenet* and no work needed to be done.

  """

  try:
    carenet_pha = CarenetPHA.objects.get(carenet=carenet, pha__email=pha.email)
    carenet_pha.delete()
  except CarenetPHA.DoesNotExist:
    pass

  return DONE



def carenet_app_permissions(request, carenet, pha):
  """ Retrieve the permissions for an app within a carenet. NOT IMPLEMENTED.

  Will return :http:statuscode:`200` always, without doing anything.
  
  """

  # Not yet implemented
  return DONE

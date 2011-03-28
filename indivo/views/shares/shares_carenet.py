"""
Indivo views -- Sharing
"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def carenet_create(request, record):
  NAME = 'name'
  if request.POST.has_key(NAME):
    carenet_name = request.POST[NAME]
    cnObj = Carenet.objects.create(name = carenet_name, record = record)
    return render_template('shares', {'share':cnObj, 'record':record}, type="xml")
  else:
    return HttpResponseBadRequest()


def carenet_list(request, record):
  carenets = Carenet.objects.filter(record=record)
  return render_template('carenets', {'carenets':carenets, 'record':record}, type="xml")

"""
Indivo views -- Sharing
"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied

NAME = 'name'

def carenet_create(request, record):
  if request.POST.has_key(NAME):
    carenet_name = request.POST[NAME]
    cnObj = Carenet.objects.create(name = carenet_name, record = record)
    return render_template('carenets', {'carenets':[cnObj], 'record':record}, type="xml")
  else:
    return HttpResponseBadRequest('Please provide a name for the carenet')

def carenet_list(request, record):
  carenets = Carenet.objects.filter(record=record)
  return render_template('carenets', {'carenets':carenets, 'record':record}, type="xml")

def carenet_delete(request, carenet):
  carenet.delete()
  return DONE

def carenet_rename(request, carenet):
  if request.POST.has_key(NAME):
    carenet.name = request.POST[NAME]
    carenet.save()
    return render_template('carenets', {'carenets': [carenet], 'record':carenet.record}, type="xml")
  else:
    return HttpResponseBadRequest('Please provide a new name for the carenet')

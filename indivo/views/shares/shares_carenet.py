"""
Indivo views -- Sharing
"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

NAME = 'name'

@transaction.commit_on_success
def carenet_create(request, record):
    """
    POST to /records/{record_id}/carenets/
    Must have a 'name' key/value pair and the name must not yet be used by this record
    """
    if request.POST.has_key(NAME):
        carenet_name = request.POST[NAME]
        try:
            cnObj = Carenet.objects.create(name = carenet_name, record = record)
        except IntegrityError:
            transaction.rollback()
            return HttpResponseBadRequest('Carenet name is already taken')
        return render_template('carenets', {'carenets':[cnObj], 'record':record}, type="xml")
    return HttpResponseBadRequest('Please provide a name for the carenet')


def carenet_list(request, record):
    carenets = Carenet.objects.filter(record=record)
    return render_template('carenets', {'carenets':carenets, 'record':record}, type="xml")


def carenet_delete(request, carenet):
    carenet.delete()
    return DONE


@transaction.commit_on_success
def carenet_rename(request, carenet):
    if request.POST.has_key(NAME):
        try:
            carenet.name = request.POST[NAME]
            carenet.save()
        except IntegrityError:
            transaction.rollback()
            return HttpResponseBadRequest('Carenet name is already taken')
        return render_template('carenets', {'carenets': [carenet], 'record':carenet.record}, type="xml")
    return HttpResponseBadRequest('Please provide a new name for the carenet')

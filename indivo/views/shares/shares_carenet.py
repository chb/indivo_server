"""
.. module:: views.sharing.shares_carenet
   :synopsis: Indivo view implementations related to carenet management

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from indivo.views.base import *
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

NAME = 'name'

@transaction.commit_on_success
def carenet_create(request, record):
    """ Create a new carenet for a record.
  
    request.POST must contain:
    
    * *name*: the label for the new carenet.

    Will return :http:statuscode:`200` with XML describing the new
    carenet on success, :http:statuscode:`400` if *name* wasn't passed
    or if a carenet named *name* already exists on this record.
    
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
    """ List all carenets for a record.

    Will return :http:statuscode:`200` with a list of carenets on success.

    """
    carenets = Carenet.objects.filter(record=record)
    return render_template('carenets', {'carenets':carenets, 'record':record}, type="xml")


def carenet_delete(request, carenet):
    """ Delete a carenet.

    Will return :http:statuscode:`200` on success.

    """

    carenet.delete()
    return DONE


@transaction.commit_on_success
def carenet_rename(request, carenet):
    """ Change a carenet's name.

    request.POST must contain:
    
    * *name*: The new name for the carenet.
    
    Will return :http:statuscode:`200` with XML describing the renamed
    carenet on success, :http:statuscode:`400` if *name* wasn't passed
    or if a carenet named *name* already exists on this record.

    """

    if request.POST.has_key(NAME):
        try:
            carenet.name = request.POST[NAME]
            carenet.save()
        except IntegrityError:
            transaction.rollback()
            return HttpResponseBadRequest('Carenet name is already taken')                  # Indivo UI relies on this string to identify the reason of the 400 being returned
        return render_template('carenets', {'carenets': [carenet], 'record':carenet.record}, type="xml")
    return HttpResponseBadRequest('Please provide a new name for the carenet')

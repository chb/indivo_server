"""
Indivo Views -- Base
"""

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.core.exceptions import *
from django.core import serializers
from django.db import transaction

from indivo.models import *
#from indivo.accesscontrol.security import *
from indivo.lib.view_decorators import marsloader, commit_on_200

import logging, datetime

# SZ: standardize
from indivo.lib import utils
from indivo.lib.utils import render_template, render_template_raw

DONE = render_template('ok', {}, type="xml")

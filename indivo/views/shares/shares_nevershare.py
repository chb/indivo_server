"""
.. module:: views.sharing.shares_nevershare
   :synopsis: Indivo view implementations related to nevershares

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

import indivo.views
from indivo.views.base import *
from indivo.views.documents.document import _render_documents, _get_document
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def document_set_nevershare(request, record, document_id):
  """ Flag a document to never be shared, anywhere.

  This overrides autoshares and existing shares, and prevents
  sharing the document in the future, until
  :py:meth:`~indivo.views.shares.shares_nevershare.document_remove_nevershare` 
  is called.

  Will return :http:statuscode:`200` on success, :http:statuscode:`404` if 
  *document_id* is invalid.

  """

  document = _get_document(document_id=document_id, record=record)
  if not document:
    raise Http404

  document.nevershare = True
  document.save()
  return DONE


def document_remove_nevershare(request, record, document_id):
  """ Remove the nevershare flag from a document.

  If a document has was shared via autoshare or explicitly, then marked
  as nevershare, this call will reactivate all previously existing shares.

  Will return :http:statuscode:`200` on success, :http:statuscode:`404` if
  *document_id* is invalid.
  
  """

  document = _get_document(document_id=document_id, record=record)
  if not document:
    raise Http404

  document.nevershare = False
  document.save()
  return DONE

"""
Indivo views -- nevershare
"""

import indivo.views
from indivo.views.base import *
from indivo.views.documents.document import _render_documents, _get_document
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def document_set_nevershare(request, record, document_id):
  """
  Flag a document as nevershare
  """
  document = _get_document(document_id=document_id, record=record)
  if not document:
    raise Http404

  document.nevershare = True
  document.save()
  return DONE


def document_remove_nevershare(request, record, document_id):
  """
  Remove nevershare flag
  """
  document = _get_document(document_id=document_id, record=record)
  if not document:
    raise Http404

  document.nevershare = False
  document.save()
  return DONE

"""
Sharing-related Utilities for Indivo
"""
from django.db.models import Q
from indivo.models import DocumentSchema, Document

def carenet_facts_filter(carenet, facts):
  ''' Filters a set of facts, removing facts that were generated from documents not shared in 'carenet'.
  Assumes that the input set of facts is a Django QuerySet, and never evaluates it.'''
  return _carenet_filter(carenet, facts, facts_p=True)


def carenet_documents_filter(carenet, documents):
  ''' Filters a set of documents, removing those not shared in 'carenet'.
  Assumes that the input set of documents is a Django QuerySet, and never evaluates it.'''
  return _carenet_filter(carenet, documents)

def document_in_carenet(carenet, doc_id):
  ''' Returns True if the passed document id corresponds to a shared document, False otherwise. '''
  return _carenet_filter(carenet, Document.objects.all()).filter(id=doc_id).exists()

def document_carenets_filter(document, carenets):
  ''' Filters a set of carenets, removing those that 'document' is not shared in.
  Assumes that the input set of carenets is a Django QuerySet, and never evaluates it.'''

  # Optimization if the doc has been nevershared
  if document.nevershare:
    return carenets.none()

  # Constrain to the record we're looking for
  carenets = carenets.filter(record=document.record)

  # The carenet has been shared with explicitly
  explicitly_shared_with = Q(carenetdocument__document=document, carenetdocument__share_p=True)

  # The carenet has been shared with implicitly via autoshares
  implicitly_shared_with = Q(carenetautoshare__type=document.type, carenetautoshare__type__isnull=False)

  # There is an exception to the autoshares
  implicit_share_exception = Q(carenetdocument__document=document, carenetdocument__share_p=False)

  # The carenet has been shared with appropriately with the document
  shared_with_doc = explicitly_shared_with | (implicitly_shared_with & ~implicit_share_exception)
  return carenets.filter(shared_with_doc)

def _carenet_filter(carenet, objs, facts_p = False):
  if carenet:  

    # All doc types the carenet autoshares with
    carenet_autoshare_types = DocumentSchema.objects.filter(carenetautoshare__carenet = carenet)

    # If we're filtering a set of Fact objects, the filters have to use the 'document' property of the objects
    if facts_p:
      explicit_args = {'document__carenetdocument__carenet':carenet, 
                       'document__carenetdocument__share_p':True,
                       'document__nevershare': False,}
      autoshared_args = {'document__type__in': carenet_autoshare_types,
                         'document__nevershare':False}
      autoshare_exception_args = {'document__carenetdocument__carenet':carenet,
                                  'document__carenetdocument__share_p': False}
    else:
      explicit_args = {'carenetdocument__carenet':carenet, 
                       'carenetdocument__share_p':True,
                       'nevershare': False,}
      autoshared_args = {'type__in': carenet_autoshare_types,
                         'nevershare':False}
      autoshare_exception_args = {'carenetdocument__carenet':carenet,
                                  'carenetdocument__share_p': False}

    # The doc is explicity shared in the carenet
    explicitly_shared = Q(**explicit_args)

    # The doc is implicity shared in the carenet via an autoshare
    implicitly_shared = Q(**autoshared_args)

    # There is no exception to the implicit autoshare
    implicit_share_exception = Q(**autoshare_exception_args)

    # The doc is shared appropriately in the carenet
    shared_in_carenet = explicitly_shared | (implicitly_shared & ~implicit_share_exception)

    # Add the filter, but don't force evaluation
    objs = objs.filter(shared_in_carenet)

  return objs

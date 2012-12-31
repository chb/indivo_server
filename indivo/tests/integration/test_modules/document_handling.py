import os
import data

from lxml import etree
from utils import *

PRD = 'prd'
RESP_DATA = 'response_data'

def test_document_handling(IndivoClient):

  try:
    # Create Admin client
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    admin_client.set_app_id(data.app_email)
    record_id = admin_client.create_record(data=data.demographics).response[PRD]['Record'][0]
    admin_client.set_record_owner(data=data.account['account_id'])

    # Create a new record by external ID, twice.
    record_id_1 = etree.XML(admin_client.put_record_ext(principal_email = data.machine_app_email, external_id = 'record_ext_foobar', data=data.demographics).response[RESP_DATA]).attrib['id']
    record_id_2 = etree.XML(admin_client.put_record_ext(principal_email = data.machine_app_email, external_id = 'record_ext_foobar', data=data.demographics).response[RESP_DATA]).attrib['id']
    if record_id_1 != record_id_2:
      raise Exception("record creation with external ID not idempotent")

    # this should fail, because of bad principal_email
    # record_id_3 = etree.XML(admin_client.put_record_ext(principal_email = data.machine_app_email + "s", external_id = 'record_ext_foobar', data=data.contact).response[RESP_DATA]).attrib['id']

    # Create Chrome client
    chrome_client = IndivoClient(data.chrome_consumer_key, data.chrome_consumer_secret)
    chrome_client.create_session(data.account)
    chrome_client.read_record(record_id=record_id)

    chrome_client.post_document(data=data.doc01)
    document_id = chrome_client.read_documents().response[PRD]['Document'][0]
    chrome_client.read_document_meta(document_id=document_id)

    document_id = chrome_client.read_documents().response[PRD]['Document'][1]
    chrome_client.set_document_status(data='reason=void1&status=void')
    chrome_client.set_document_status(data='reason=archive&status=archived')
    chrome_client.set_document_status(data='reason=firstactive&status=active')
    chrome_client.set_document_status(data='reason=void2&status=void')
    chrome_client.read_document_status_history()

    chrome_client.post_document(data=data.doc02)
    document_id = chrome_client.read_documents().response[PRD]['Document'][0]
    #chrome_client.delete_document() : No longer used

    chrome_client.read_documents(parameters={'status':'active'})
    chrome_client.read_documents(parameters={'status':'void'})
    chrome_client.read_documents()

    chrome_client.post_document(data=data.doc03)
    document_id = chrome_client.read_documents().response[PRD]['Document'][0]
    chrome_client.read_document_meta(document_id=document_id)

    chrome_client.read_documents(parameters={'type':data.doc_type})
    chrome_client.read_document_versions(document_id=document_id)
    chrome_client.post_document_label(document_id=document_id, data=data.label)
    data_docs = [data.doc08, data.doc11, data.doc12, data.doc02, data.doc05]
    for data_doc in data_docs:
      response = chrome_client.replace_document(document_id=document_id, data=data_doc).response
      chrome_client.post_document_relate_given(rel_type='annotation', data=data.doc08)
      document_id = response[PRD]['Document'][0]

    assert_200(chrome_client.get_document_relate(rel_type='annotation'))

    document_id = chrome_client.post_document(data=data.allergy).response[PRD]['Document'][0]
    chrome_client.set_document_status(data='reason=allergy not correct&status=active')

    # this should fail
    assert_400(chrome_client.set_document_status(data='reason=allergy not correct&status=activated'), "bad status should not be allowed to be set on doc")

    chrome_client.post_document(data=data.doc00)
    chrome_client.read_allergies()

    chrome_client.post_document(data=data.problem)
    chrome_client.read_documents(parameters={'type':'http://indivo.org/vocab/xml/documents#Problem'})

    # try out documents that should be wrong
    assert_400(chrome_client.post_document(data = data.malformed_allergy), "Malformed Allergy - wrong schema")
    
    # Delete all documents related to this record
    # chrome_client.delete_documents()

  except Exception, e:
    return False, e
  return True

 

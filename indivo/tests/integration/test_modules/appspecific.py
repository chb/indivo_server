"""
Test proper partition of app-specific and app-record-specific

Ben Adida
2010-09-13
"""

import data

from utils import *

PRD = 'prd'

def test_appspecific(IndivoClient):
    """
    ensure that app-specific and app-record-specific data are 
    properly partitioned
    """
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)

    # create a record and authorize a PHA to access it
    record = parse_xml(admin_client.create_record(data=data.demographics))
    record_id = xpath(record, '/Record/@id')[0]
    token = admin_client.setup_app(record_id=record_id, app_id=data.app_email).response['prd']

    pha_client = IndivoClient(data.app_email, data.app_secret)

    # store an app-specific document
    appspecific_doc = parse_xml(pha_client.post_app_document_ext(app_id = data.app_email, external_id='foobar_partition_appspecific', data=data.allergy))

    # store an app-record-specific document
    pha_client.update_token(token)
    apprecordspecific_doc = parse_xml(pha_client.put_recapp_document_ext(record_id = record_id, app_id = data.app_email, external_id='foobar_partition_apprecordspecific', data=data.allergy))

    # get it by metadata
    apprecordspecific_doc_check = parse_xml(pha_client.read_recapp_document_ext_meta(record_id = record_id, app_id = data.app_email, external_id='foobar_partition_apprecordspecific'))
    
    def check_lists():
        pha_client = IndivoClient(data.app_email, data.app_secret)

        # get the list of documents that are available in app-specific
        appspecific_list = parse_xml(pha_client.read_app_documents(app_id = data.app_email))
        
        # get the list of documents that are available in 
        pha_client.update_token(token)
        apprecordspecific_list = parse_xml(pha_client.get_recapp_documents(record_id = record_id, app_id = data.app_email))
        
        # make sure they are not visible to each other's call
        assert xpath(apprecordspecific_doc, '/Document/@id')[0] in xpath(apprecordspecific_list, '/Documents/Document/@id')
        assert xpath(appspecific_doc, '/Document/@id')[0] in xpath(appspecific_list, '/Documents/Document/@id')
        assert xpath(appspecific_doc, '/Document/@id')[0] not in xpath(apprecordspecific_list, '/Documents/Document/@id')
        assert xpath(apprecordspecific_doc, '/Document/@id')[0] not in xpath(appspecific_list, '/Documents/Document/@id')
        

    check_lists()
    
    # create a second record and authorize the PHA again
    record_2 = parse_xml(admin_client.create_record(data=data.demographics))
    record_id_2 = xpath(record, '/Record/@id')[0]
    token = admin_client.setup_app(record_id=record_id_2, app_id=data.app_email).response['prd']

    # add an app-record-specific doc in there, shouldn't affect either of the other two, and should be able to use the same external_id
    pha_client.update_token(token)
    apprecordspecific_doc_2 = parse_xml(pha_client.put_recapp_document_ext(record_id = record_id_2, app_id = data.app_email, external_id='foobar_partition_apprecordspecific', data=data.immunization))
    
    check_lists()

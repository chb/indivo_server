import data

from utils import assert_403, assert_404, assert_200, parse_xml, xpath

PRD = 'prd'

def test_sharing(IndivoClient):
  DS = 'ds' 

  def get_datastore(obj):
    if hasattr(obj, DS):
      return getattr(obj, DS).values()
    return False

  def set_datastore(obj, **kwargs):
    if hasattr(obj, DS):
      ds = getattr(obj, DS)
      for kwarg, value in kwargs.items():
        if hasattr(ds, kwarg):
          setattr(ds, kwarg, value)
      return obj
    raise ValueError

  def alice_setup(record_id, bob_account_id):

    allergy_type = {'type' : 'http://indivo.org/vocab/xml/documents#Allergy'}

    alice_chrome_client = IndivoClient('chrome', 'chrome')
    alice_chrome_client.create_session(data.account)
    alice_chrome_client.read_record(record_id=record_id)
    alice_chrome_client.get_account_permissions(account_id=data.account['account_id'])

    alice_chrome_client.get_account_records(account_id = data.account['account_id'])

    # Alice posts a document
    # (We save the first doc instead of zero 
    #   due to the contact doc already in alice's account)
    alice_chrome_client.post_document(data=data.doc01)
    document_id = alice_chrome_client.read_documents().response[PRD]['Document'][1]

    # Save the document_id in the client's datastore
    alice_chrome_client.ds.document_id = document_id

    # Save the first carenet_id in the client's datastore
    carenet_id = alice_chrome_client.get_record_carenets().response[PRD]['Carenet'][0]

    # post four documents to Alice's record, 2 allergies and 2 immunizations
    document_1_id = xpath(parse_xml(alice_chrome_client.post_document(data=data.allergy00)), "/Document/@id")[0]
    document_2_id = xpath(parse_xml(alice_chrome_client.post_document(data=data.allergy01)), "/Document/@id")[0]
    document_3_id = xpath(parse_xml(alice_chrome_client.post_document(data=data.immunization)), "/Document/@id")[0]
    document_4_id = xpath(parse_xml(alice_chrome_client.post_document(data=data.immunization2)), "/Document/@id")[0]

    # and one more to test nevershare
    document_5_id = xpath(parse_xml(alice_chrome_client.post_document(data=data.allergy02)), "/Document/@id")[0]

    # auto-share allergies
    alice_chrome_client.post_autoshare(data=allergy_type, carenet_id=carenet_id)

    assert_200(alice_chrome_client.get_autoshare_bytype_all(record_id=record_id))

    # unshare that one allergy, which should negate the autoshare
    alice_chrome_client.delete_carenet_document(record_id = record_id, document_id = document_2_id, carenet_id=carenet_id)

    # nevershare the third allergy
    alice_chrome_client.document_nevershare_set(record_id = record_id, document_id = document_5_id)

    # immunizations are individually shared (well only one of them)
    alice_chrome_client.post_carenet_document(document_id = document_3_id, carenet_id=carenet_id)
    
    # Alice shares her contact document(s) with the carenet
    contact_doc = parse_xml(alice_chrome_client.read_documents(record_id = record_id, parameters={'type':'Contact'}))
    for doc_id in xpath(contact_doc, '/Documents/Document/@id'):
      alice_chrome_client.post_carenet_document(record_id = record_id, document_id = doc_id, carenet_id = carenet_id)

    # Alice adds bob_account_id to carenet[0]
    alice_chrome_client.post_carenet_account(carenet_id = carenet_id, data='account_id=' + bob_account_id + '&write=false')

    # Review all accounts within carenet[0]
    assert xpath(parse_xml(alice_chrome_client.get_carenet_accounts(carenet_id = carenet_id)), '/CarenetAccounts')
    alice_chrome_client.get_carenet_apps(carenet_id = carenet_id)

    alice_chrome_client.read_allergies(record_id = record_id)

    # Finally, return the carenet_id, document_id
    # in order to check Bob's access
    # and a second document that is disallowed
    return carenet_id, [document_1_id, document_3_id], [document_2_id, document_4_id, document_5_id]

  def bob_setup(bob_account_id, record_id, carenet_id, allowed_docs, disallowed_docs):
    bob_chrome_client = IndivoClient('chrome', 'chrome')
    bob_chrome_client.create_session(data.account02)

    # SZ: Bob should NOT be able to read the docs directly in the record
    for doc_id in allowed_docs+disallowed_docs:
      assert_403(bob_chrome_client.read_document(record_id=record_id, document_id=doc_id))

    assert_403(bob_chrome_client.get_record_carenets(record_id=record_id))

    # Bob should be able to read the allowed docs
    for doc_id in allowed_docs:
      assert_200(bob_chrome_client.get_carenet_document(carenet_id = carenet_id, document_id = doc_id))

    # Bob should not be able to read the disallowed docs
    for doc_id in disallowed_docs:
      assert_404(bob_chrome_client.get_carenet_document(carenet_id = carenet_id, document_id = doc_id))
    
    # Bob should be able to list docs in the carenet
    carenet_documents_list = bob_chrome_client.get_carenet_documents(carenet_id = carenet_id).response[PRD]['Document']

    # with a parameter
    carenet_documents_list = bob_chrome_client.get_carenet_documents(carenet_id = carenet_id, parameters={'type': 'http://indivo.org/vocab/xml/documents#Allergy'}).response[PRD]['Document']

    # Read carenet allergies
    assert_200(bob_chrome_client.read_carenet_allergies(carenet_id = carenet_id))
    assert_200(bob_chrome_client.read_carenet_problems(carenet_id = carenet_id))

    # Read the contact document, this should work
    contact_doc = parse_xml(bob_chrome_client.read_carenet_special_document(carenet_id = carenet_id, special_document='contact'))
    contact_name = xpath(contact_doc, '/ns:Contact/ns:name/ns:fullName/text()', namespaces={'ns':'http://indivo.org/vocab/xml/documents#'})
    assert(contact_name)

    bob_chrome_client.get_account_permissions(account_id=bob_account_id)
    bob_chrome_client.get_carenet_account_permissions(carenet_id= carenet_id,
                                                      record_id=record_id, 
                                                      account_id=bob_account_id)

    # Not yet implemented
    #bob_chrome_client.get_carenet_app_permissions(account_id=bob_account_id)

    return True


  def admin_setup(bob_account_id):

    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    admin_client.set_app_id(data.app_email)

    # Create a record for Alice and set her at the owner
    record_id = admin_client.create_record(data=data.contact).response[PRD]['Record'][0]
    admin_client.set_record_owner(data=data.account['account_id'])

    # Create a basic set of carenets
    carenet_names = ['Family2', 'Friends2', 'School/Office']
    for cname in carenet_names:
      admin_client.create_carenet(data='name=' + cname)

    # Check to make sure the admin can list the carenets and the accounts within each one
    carenets = xpath(parse_xml(admin_client.get_record_carenets(record_id = record_id)),'/Carenets/Carenet/@id')

    for carenet_id in carenets:
      assert len(xpath(parse_xml(admin_client.get_carenet_accounts(carenet_id = carenet_id)), '/CarenetAccounts')) > 0

    return record_id

  bob_account_id = 'benadida@informedcohort.org'

  # Admin spawning carenets under Alice's newly created record
  record_id = admin_setup(bob_account_id)
  
  # Given Bob's account id and a record that has been set up for her
  # Alice gives Bob the document_id that she'd like to share with him
  #   Even though Alice gives Bob a document_id, Bob has the ability
  #   to read all documents within the carenet that Alice added him to
  # 2010-09-13 now Alice also shares her contact URL and we check
  #    that Bob can read it at the special URL
  carenet_id, allowed_documents, disallowed_documents = alice_setup(record_id, bob_account_id)
  return bob_setup(bob_account_id, record_id, carenet_id, allowed_documents, disallowed_documents)


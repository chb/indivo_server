"""
Do a bunch of security tests

Ben Adida
2010-08-27
"""
import os, cgi, uuid
import data

from lxml import etree
from django.utils import simplejson
from utils import *

PRD = 'prd'
RESP_DATA = 'response_data'

def test_client_expect_no_access(client, record_id, document_id, run_special_admin_calls=True):
    """
    run tests on a client with a given record_id where the client should have zero access
    to that record. The document ID is a real document inside that record, which shouldn't be allowed to be accessed of course.
    """

    # commented out for now: admin apps should be able to read records that they created
    #assert_403(client.read_record(record_id = record_id))

    if run_special_admin_calls:
        # admin client shouldn't be able to add a document, but TEMPORARILY we're allowing this
        # but NOT on a record not created by the admin app
        assert_403(client.post_document(record_id=record_id, data=data.doc01))
        
        # we DO allow an admin client to check the shares on a record it has created,
        # but not on another record
        assert_403(client.get_shares(record_id=record_id))

        # admin clients querying list of carenets... kosher?
        # should not be able to list carenets, see sharing, etc..
        assert_403(client.get_record_carenets(record_id=record_id))
        assert_403(client.create_carenet(record_id=record_id, data={'name':'foobar'}))
        assert_403(client.get_autoshare(record_id=record_id))

        assert_403(client.setup_app(record_id=record_id, app_id=data.app_email))

        assert_403(client.message_record(record_id=record_id, message_id= str(uuid.uuid1()), data={'subject':'foo','body':'bar', 'num_attachments': 1}))
        assert_403(client.message_record_attachment(record_id=record_id, message_id= str(uuid.uuid1()), attachment_num="1", data="<foo>bar</foo>"))

    assert_403(client.read_documents(record_id=record_id))

    assert_403(client.post_document_ext(record_id=record_id, app_id=data.app_email, external_id= "foobar-ext-fail", data=data.doc01))

    # even when the app_email matches the client, this should give no access
    assert_403(client.get_recapp_documents(record_id=record_id, app_id = data.app_email))

    # FIXME: test the replace call once it returns
    # assert_403(client.replace_document(record_id, document_id=document_id, data=data.doc02))

    assert_403(client.read_document(record_id=record_id, document_id=document_id))
    assert_403(client.read_document_meta(record_id=record_id, document_id=document_id))

    assert_403(client.read_document_versions(record_id=record_id, document_id=document_id))

    assert_403(client.set_document_status(record_id=record_id, document_id=document_id, data='reason=void1&status=void'))
    assert_403(client.read_document_status_history(record_id=record_id, document_id=document_id))

    reports = ['read_equipment', 'read_procedures', 
               ['read_measurements', {'lab_code':'HBA1C'}], 'read_labs']
    for report in reports:
        extra_params = {}
        if type(report) == list:
            extra_params = report[1]
            report = report[0]
        assert_403(getattr(client, report)(**combine_dicts({'record_id':record_id}, extra_params)))


def test_account_admin_calls(client, account_id):
    """
    the following calls should be doable only by an admin app on an account
    only an admin app can add auth system, set password, initialize account, and send the secret
    """

    assert_403(client.add_auth_system(account_id= account_id, data={'system':'password', 'username':'foo', 'password': 'bar'}))

    assert_403(client.account_set_password(account_id= account_id, data={'password': 'foo'}))
 
    # hard to test this one since the primary secret being wrong should give 403 too, should make this better
    assert_403(client.account_initialize(account_id= account_id, primary_secret='foobar'))

    assert_403(client.account_secret_resend(account_id = account_id))

    assert_403(client.account_set_state(account_id = account_id, data={'state': 'active'}))

    assert_403(client.account_primary_secret(account_id = account_id))

    assert_403(client.check_account_secrets(account_id = account_id, primary_secret='foo'))

    assert_403(client.account_forgot_password(account_id = account_id))

    assert_403(client.account_search(data = {'contact_email':  'foo@foo.com'}))

    assert_403(client.put_record_ext(principal_email = data.machine_app_email, external_id = 'record_ext_foobar', data=data.contact))

    assert_403(client.message_account(account_id = account_id, data = {'subject':'foo', 'body':'bar'}))


def test_chrome_session_calls(client, account_id):
    """
    calls that should only be permissible to a chrome session that *is* the account in question and has full access to the record
    """

    # view account inbox
    assert_403(client.account_inbox(account_id = account_id))
        
    # view account inbox message
    assert_403(client.account_inbox_message(account_id = account_id, message_id='foo'))

    # accept attachment into record
    assert_403(client.account_inbox_message_attachment_accept(account_id = account_id, message_id='foo', attachment_num="1"))

    # view account healthfeed
    assert_403(client.account_notifications(account_id = account_id))

    # change password (FIXME: hard to test this, need something more specific)
    assert_403(client.account_change_password(account_id = account_id, data={'old':'foo', 'new':'bar'}))


def test_security(IndivoClient):

    account_id = data.account['account_id']
    account_id_2 = data.account02['account_id']

    ##
    ## Create a Record to see if others can access it
    ##
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    admin_client.set_app_id(data.app_email)
    record_id = admin_client.create_record(data=data.contact).response[PRD]['Record'][0]
    admin_client.post_document(record_id=record_id, data=data.doc01)
    admin_client.set_record_owner(data=account_id)

    # create another different record and put some docs in it
    chrome_client = IndivoClient(data.chrome_consumer_key, data.chrome_consumer_secret)
    record2_id = chrome_client.create_record(data=data.contact).response[PRD]['Record'][0]
    chrome_client.set_record_owner(record_id = record2_id, data= account_id_2)

    # put some documents into the first and second records
    chrome_client.create_session(data.account)
    document_id = chrome_client.post_document(record_id=record_id, data=data.allergy).response['prd']['Document'][0]
    chrome_client.post_document(record_id=record_id, data=data.allergy)
    chrome_client.post_document(record_id=record_id, data=data.allergy)

    chrome_client = IndivoClient(data.chrome_consumer_key, data.chrome_consumer_secret)
    chrome_client.create_session(data.account02)
    document2_id = chrome_client.post_document(record_id=record2_id, data=data.allergy).response['prd']['Document'][0]
    chrome_client.post_document(record_id=record2_id, data=data.allergy)
    chrome_client.post_document(record_id=record2_id, data=data.allergy)


    # other than the record owner, no one should have access

    ##
    ## A bogus client, should have access to nothing
    ##
    bogus_client = IndivoClient("foo","bar")

    assert_403(bogus_client.create_record(data=data.contact))

    test_client_expect_no_access(bogus_client, record_id, document_id)

    # Creating a session should raise a 403
    try:
        token = bogus_client.create_session(data.account)
        if token:
            raise AssertionError("shouldn't be able to create a session: got a valid token.")    
    except IOError as e:
        if e.errno  != 403:
            raise AssertionError("shouldn't be able to create a session: got a non 403 response.")

    test_account_admin_calls(bogus_client, account_id)

    test_chrome_session_calls(bogus_client, account_id)

    # view account
    assert_403(bogus_client.account_info(account_id = account_id))


    ##
    ## Admin Client
    ##

    test_client_expect_no_access(admin_client, record_id, document_id, run_special_admin_calls=False)
    test_client_expect_no_access(admin_client, record2_id, document2_id, run_special_admin_calls=False)

    test_chrome_session_calls(admin_client, account_id)

    ##
    ## Chrome client = user
    ## 
    chrome_client = IndivoClient(data.chrome_consumer_key, data.chrome_consumer_secret)
    chrome_client.create_session(data.account)

    # no access to other record
    test_client_expect_no_access(chrome_client, record2_id, document2_id)

    # chrome client with session is NO LONGER an admin client
    test_account_admin_calls(chrome_client, account_id)

    # chrome client shouldn't access the other account
    test_chrome_session_calls(chrome_client, account_id_2)

    # view other account
    assert_403(chrome_client.account_info(account_id = account_id_2))

    ##
    ## User App 
    ## 
    
    # an app that has not been authorized
    pha_client = IndivoClient(data.app_email, data.app_secret)
    pha_client.set_app_id(data.app_email)
    pha_client.update_token({'oauth_token': "foo", "oauth_token_secret": "bar"})

    test_client_expect_no_access(pha_client, record_id, document_id)
    test_client_expect_no_access(pha_client, record2_id, document2_id)

    # authorize it for one record
    token = admin_client.setup_app(record_id=record_id, app_id=data.app_email).response['prd']

    # make sure records are still inaccessible because token not set
    test_client_expect_no_access(pha_client, record2_id, document2_id)
    test_client_expect_no_access(pha_client, record_id, document_id)
    
    # no admin or chrome session calls before token
    test_account_admin_calls(pha_client, account_id)
    test_chrome_session_calls(pha_client, account_id)
    assert_403(pha_client.account_info(account_id = account_id))

    # set the token
    pha_client.update_token(token)

    # no admin or chrome session calls after token
    test_account_admin_calls(pha_client, account_id)
    test_chrome_session_calls(pha_client, account_id)
    assert_403(pha_client.account_info(account_id = account_id))

    # make sure other record still inaccessible
    test_client_expect_no_access(pha_client, record2_id, document2_id)

    ##
    ## put a user in a carenet and see if he is successfully blocked from other carenets
    ##
    def create_account(account_email, username, password):
        # create an account
        account_id = xpath(parse_xml(admin_client.create_account({'user_email' : account_email, 'primary_secret_p' : '1'})['response_data']), '/Account/@id')[0]

        # get the primary secret
        primary_secret_resp = admin_client.account_primary_secret(account_id = account_email)
        parsed_resp = parse_xml(primary_secret_resp)
        primary_secret = parsed_resp.text

        # initialize it
        admin_client.account_initialize(account_id= account_email, primary_secret=primary_secret)

        # set password
        admin_client.add_auth_system(account_id= account_email, data={'system':'password', 'username':username, 'password': password})

        return account_id

    def login_as(username, password):
        chrome_client = IndivoClient(data.chrome_consumer_key, data.chrome_consumer_secret)
        chrome_client.create_session({'username':username,'user_pass': password})
        return chrome_client

    owner = create_account('security-account-owner@indivo.org', 'owner','owner-password')
    friend = create_account('security-account-sharer@indivo.org', 'friend', 'friend-password')

    record_id = admin_client.create_record(data=data.contact).response[PRD]['Record'][0]
    admin_client.set_record_owner(record_id = record_id, data=owner)

    chrome_client = login_as('owner', 'owner-password')

    # get the list of carenets
    carenets = chrome_client.get_record_carenets(record_id = record_id).response[PRD]['Carenet']
    carenet_id = carenets[0]
    other_carenet_id = carenets[1]

    # add the friend to the carenet
    chrome_client.post_carenet_account(carenet_id = carenet_id, data={'account_id': friend, 'write': 'false'})
    
    # login as the friend
    chrome_client = login_as('friend', 'friend-password')

    # read other carenet documents?
    assert_403(chrome_client.get_carenet_documents(carenet_id = other_carenet_id))
    assert_403(chrome_client.get_carenet_apps(carenet_id = other_carenet_id))

    ##
    ## make sure an app not in a given carenet is not visible to someone in that carenet
    ##

    # authorize the app into the record
    token = admin_client.setup_app(record_id=record_id, app_id=data.app_email).response['prd']

    # should not be visible at this point
    def check_app():
        app_list = simplejson.loads(chrome_client.get_carenet_apps(carenet_id=carenet_id).response['response_data'])
        assert len(app_list) == 0, "some apps are in there:\n%s" % etree.tostring(app_list[0])

    # now add the app to the other carenet
    chrome_client = login_as('owner', 'owner-password')
    chrome_client.post_carenet_app(carenet_id = other_carenet_id, app_id = data.app_email)

    # still not visible, cause friend is in main carenet, not other carenet
    chrome_client = login_as('friend', 'friend-password')
    check_app()

    # oauth process
    def do_oauth(chrome_client, app_id, app_secret, record_id=None, carenet_id=None):
        """
        perform the whole oauth process up until and including the request token approve
        most of the time we're checking that that one fails
        """

        # get the request token
        app_client = IndivoClient(app_id, app_secret)
        app_client.set_app_id(app_id)
        params = {'oauth_callback': 'oob'}

        approve_params = {}
        if record_id:
            params['indivo_record_id'] = record_id
            approve_params['record_id'] = record_id
        if carenet_id:
            params['indivo_carenet_id'] = carenet_id
            approve_params['carenet_id'] = carenet_id

        rt = app_client.get_request_token(data=params).response['prd']

        # claim it and try to approve it, should fail
        chrome_client.claim_request_token(request_token = rt['oauth_token'])
        return chrome_client.approve_request_token(request_token = rt['oauth_token'], data=approve_params)


    ## app cannot be activated by the friend in either carenet at this point,
    ## since the app is not in the carenet
    assert_403(do_oauth(chrome_client, data.app_email, data.app_secret, carenet_id = other_carenet_id))
    assert_403(do_oauth(chrome_client, data.app_email, data.app_secret, carenet_id = carenet_id))

    chrome_client = login_as('owner', 'owner-password')

    ## what happens if the owner themselves tries to activate in a carenet?
    ## right now this gives a 403, but that might not be the right thing.
    assert_403(do_oauth(chrome_client, data.app_email, data.app_secret, carenet_id = carenet_id))

    # put it in this carenet, still shouldn't be able to activate it in other carenet
    # now add the app to the other carenet
    chrome_client.post_carenet_app(carenet_id = carenet_id, app_id = data.app_email)

    chrome_client = login_as('friend', 'friend-password')
    assert_403(do_oauth(chrome_client, data.app_email, data.app_secret, carenet_id = other_carenet_id))

    ## test the oauth process for non-chrome app, request token claiming and such
    ## everything else should work, the only problem is that admin_client shouldn't be able to claim or approve the token
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)    
    assert_403(do_oauth(admin_client, data.app_email, data.app_secret, carenet_id = carenet_id))

    ## test oauth process for non-user-app, should fail immediately
    assert_403(admin_client.get_request_token(data={'oauth_callback':'oob'}))

    ## test oauth process by trying to have a different app exchange the token for the current app
    approved_rt = do_oauth(chrome_client, data.app_email, data.app_secret, carenet_id = carenet_id)

    ## make an account anything other than "active", and make sure it's not possible to login
    chrome_client = IndivoClient(data.chrome_consumer_key, data.chrome_consumer_secret)
    
    for state in ['disabled', 'retired']:
        chrome_client.account_set_state(account_id = data.account['account_id'], data={'state': state})

        try:
            token = chrome_client.create_session(data.account)
            if token:
                raise AssertionError("shouldn't be able to log in for a user in state %s: got a valid token.")
        except IOError as e:
            if e.errno  != 403:
                raise AssertionError("shouldn't be able to log in for a user in state %s: got a non 403 response.")

    ## test account permissions: messaging, change password



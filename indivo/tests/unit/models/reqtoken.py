from indivo.tests.internal_tests import enable_transactions
from base import TokenModelUnitTests
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.app import TEST_USERAPPS
from indivo.models import ReqToken
from django.db import IntegrityError, transaction

import datetime

class ReqTokenModelUnitTests(TokenModelUnitTests):
    def setUp(self):
        super(ReqTokenModelUnitTests,self).setUp()
        
        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # A record for that account
        self.record = self.createRecord(TEST_RECORDS, 1, owner=self.account)

        # An app
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # default args for constructing a token
        token, secret = self.generate_token_and_secret()
        self.args = {
            'token':token,
            'token_secret':secret,
            'verifier': self.generate_random_string(),
            'oauth_callback': self.app.callback_url,
            'pha': self.app,
            'record':self.record,
            'authorized_at':None,
            'authorized_by':None,
            'share':None
            }

    def tearDown(self):
        super(ReqTokenModelUnitTests,self).tearDown()

    @enable_transactions
    def test_construction(self):
        
        # should construct normally
        try:
            rt = ReqToken.objects.create(**self.args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create ReqToken normally')
        else:
            self.assertEqual(rt, ReqToken.objects.get(pk=rt.pk))
        
    def test_save(self):
        rt = ReqToken(**self.args)
        self.assertEqual(rt.email, '')
        rt.save()
        self.assertEqual(rt.email, '%s@requesttokens.indivo.org'%rt.token)

    def test_effective_principal(self):
        rt = ReqToken.objects.create(**self.args)
        self.assertEqual(rt.effective_principal, self.app)
    
    def test_authorized(self):
        rt = ReqToken.objects.create(**self.args)
        self.assertFalse(rt.authorized)
        rt.authorized_at = datetime.datetime.now()
        self.assertTrue(rt.authorized)

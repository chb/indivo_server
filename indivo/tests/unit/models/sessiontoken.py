import datetime

from django.db import IntegrityError, transaction
from django.utils import timezone

from indivo.tests.internal_tests import enable_transactions
from base import TokenModelUnitTests
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.models import SessionToken

SESSION_TOKEN_EXPIRATION = 30 # minutes until a session token should expire


class SessionTokenModelUnitTests(TokenModelUnitTests):
    def setUp(self):
        super(SessionTokenModelUnitTests,self).setUp()
        
        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # default args for constructing a token
        token, secret = self.generate_token_and_secret()
        self.args = {
            'token':token,
            'secret':secret,
            'user':self.account,
            'expires_at':None,
            }

    def tearDown(self):
        super(SessionTokenModelUnitTests,self).tearDown()

    @enable_transactions
    def test_construction(self):
        
        # should construct normally
        try:
            st = SessionToken.objects.create(**self.args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create SessionToken normally')
        else:
            self.assertEqual(st, SessionToken.objects.get(pk=st.pk))
        
    def test_approved_p(self):
        st = SessionToken.objects.create(**self.args)
        self.assertTrue(st.approved_p)

    def test_save(self):
        st = SessionToken(**self.args)
        self.assertEqual(st.expires_at, None)

        now = timezone.now()
        st.save()
        self.assertNotEqual(st.expires_at, None)
        
        # Make sure the expiration time falls within a minute of the expected
        # Can't use assertLessEqual or assertGreaterEqual for python2.6 compatibility
        self.assertTrue(st.expires_at <= now+datetime.timedelta(minutes=SESSION_TOKEN_EXPIRATION+1))
        self.assertTrue(st.expires_at >= now+datetime.timedelta(minutes=SESSION_TOKEN_EXPIRATION-1))

class SessionRequestTokenModelUnitTests(TokenModelUnitTests):
    def setUp(self):
        super(SessionRequestTokenModelUnitTests,self).setUp()
        
        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # default args for constructing a token
        token, secret = self.generate_token_and_secret()
        self.args = {
            'token':token,
            'token':secret,
            'user':self.account,
            'approved_p':False
            }

    def tearDown(self):
        super(SessionRequestTokenModelUnitTests,self).tearDown()

    @enable_transactions
    def test_construction(self):
        
        # should construct normally
        try:
            st = SessionToken.objects.create(**self.args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create SessionToken normally')
        else:
            self.assertEqual(st, SessionToken.objects.get(pk=st.pk))

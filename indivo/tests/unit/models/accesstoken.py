from base import TokenModelUnitTests
from indivo.tests.internal_tests import enable_transactions
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.app import TEST_AUTONOMOUS_APPS
from indivo.models import AccessToken, Carenet
from django.db import IntegrityError, transaction

import random, string

class AccessTokenModelUnitTests(TokenModelUnitTests):
    def setUp(self):
        super(AccessTokenModelUnitTests, self).setUp()

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)

        # A record for the account, with a couple carenets
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        self.carenets = Carenet.objects.filter(record=self.record)[:2]

        # An unshared account
        self.with_account = self.createAccount(TEST_ACCOUNTS, 2)

        # A proxying app, with our record shared to it.
        self.app = self.createUserApp(TEST_USERAPPS, 0)
        self.share = self.addAppToRecord(record=self.record, with_pha=self.app)

        # Another proxying app, with just a carenet shared to it.
        self.c_app = self.createUserApp(TEST_USERAPPS, 1)
        self.c_share = self.addAppToRecord(record=self.record, with_pha=self.c_app, carenet=self.carenets[0])

        # A proxying autonomous app, with our record shared to it.
        self.a_app = self.createUserApp(TEST_AUTONOMOUS_APPS, 0)
        self.a_share = self.addAppToRecord(record=self.record, with_pha=self.a_app)

    def tearDown(self):
        super(AccessTokenModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # Should construct normally
        token, secret = self.generate_token_and_secret()
        args = {'token': token,
                'token_secret': secret,
                'share': self.share,
                'account': self.account,
                'carenet': None,
                }
        try:
            at = AccessToken.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not construct account full share')
        else:
            self.assertEqual(at, AccessToken.objects.get(pk=at.pk))

        # Should construct normally when tied to a carenet
        token, secret = self.generate_token_and_secret()
        args = {'token': token,
                'token_secret': secret,
                'share': self.c_share,
                'account': self.account,
                'carenet': self.carenets[0],
                }
        try:
            at = AccessToken.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not construct account full share')
        else:
            self.assertEqual(at, AccessToken.objects.get(pk=at.pk))

        # Should construct normally without an account
        token, secret = self.generate_token_and_secret()
        args = {'token': token,
                'token_secret': secret,
                'share': self.a_share,
                'account': None,
                'carenet': None,
                }
        try:
            at = AccessToken.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not construct account full share')
        else:
            self.assertEqual(at, AccessToken.objects.get(pk=at.pk))

    def test_accesscontrol(self):

        # Build a token, for an account proxied by an app
        token, secret = self.generate_token_and_secret()
        args = {'token': token,
                'token_secret': secret,
                'share': self.share,
                'account': self.account,
                'carenet': None,
                }
        at = AccessToken.objects.create(**args)
        
        self.assertTrue(at.isProxiedByApp(self.app))
        self.assertFalse(at.isProxiedByApp(self.c_app))
        self.assertFalse(at.isProxiedByApp(self.a_app))

        self.assertTrue(at.scopedToRecord(self.record))

        self.assertFalse(at.isInCarenet(self.carenets[0]))
        self.assertFalse(at.isInCarenet(self.carenets[1]))
        
        self.assertEqual(at.effective_principal, self.account)

        # Build a token, for an account proxied by an app, tied to a carenet
        token, secret = self.generate_token_and_secret()
        args = {'token': token,
                'token_secret': secret,
                'share': self.c_share,
                'account': self.account,
                'carenet': self.carenets[0],
                }
        at = AccessToken.objects.create(**args)

        self.assertTrue(at.isProxiedByApp(self.c_app))
        self.assertFalse(at.isProxiedByApp(self.app))
        self.assertFalse(at.isProxiedByApp(self.a_app))

        self.assertFalse(at.scopedToRecord(self.record))
        
        self.assertTrue(at.isInCarenet(self.carenets[0]))
        self.assertFalse(at.isInCarenet(self.carenets[1]))
                        
        self.assertEqual(at.effective_principal, self.account)
       
        # Build a token, for an autonomous app
        token, secret = self.generate_token_and_secret()
        args = {'token': token,
                'token_secret': secret,
                'share': self.a_share,
                'account': None,
                'carenet': None,
                }
        at = AccessToken.objects.create(**args)

        self.assertFalse(at.isProxiedByApp(self.c_app))
        self.assertFalse(at.isProxiedByApp(self.app))
        self.assertFalse(at.isProxiedByApp(self.a_app))

        self.assertTrue(at.scopedToRecord(self.record))
        
        self.assertFalse(at.isInCarenet(self.carenets[0]))
        self.assertFalse(at.isInCarenet(self.carenets[1]))

        self.assertEqual(at.effective_principal, self.a_app)

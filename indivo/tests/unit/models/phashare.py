from indivo.tests.internal_tests import enable_transactions
from base import TokenModelUnitTests
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.app import TEST_USERAPPS, TEST_AUTONOMOUS_APPS
from indivo.models import PHAShare
from django.db import IntegrityError, transaction

class PHAShareModelUnitTests(TokenModelUnitTests):
    def setUp(self):
        super(PHAShareModelUnitTests, self).setUp()

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A record for the account, and one of its default carenets
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        self.carenet = self.record.carenet_set.all()[0]

        # An account to grant access to
        self.with_account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # A record w/ carenet for the with_account, not shared
        self.with_record = self.createRecord(TEST_RECORDS, 1, owner=self.with_account)
        self.with_carenet = self.with_record.carenet_set.all()[0]

        # A recipient app
        self.with_pha = self.createUserApp(TEST_USERAPPS, 0)

        # A recipient autonomous app
        self.a_with_pha = self.createUserApp(TEST_AUTONOMOUS_APPS, 0)
        
    def tearDown(self):
        super(PHAShareModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # Should construct normally, with or without carenets
        args = {'record': self.record,
                'with_pha': self.with_pha,
                'carenet': self.carenet
                }
        try:
            ps = PHAShare.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not construct pha share')
        except:
            self.fail('Could not construct pha share')
        else:
            self.assertEqual(ps, PHAShare.objects.get(pk=ps.pk))

        args['with_pha'] = self.a_with_pha
        args['carenet'] = None
        try:
            ps = PHAShare.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not construct pha share with a carenet')
        except:
            self.fail('Could not construct pha share with a carenet')
        else:
            self.assertEqual(ps, PHAShare.objects.get(pk=ps.pk))

        # Should break if the same record is shared twice with the same app
        try:
            ps = PHAShare.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Shared a record with the same pha twice')
        
    def test_new_access_token(self):

        # Share our non-autonomous pha
        pha_share = self.addAppToRecord(self.record, self.with_pha)

        # build an access token for a foreign account to access the app
        token, secret = self.generate_token_and_secret()
        at = pha_share.new_access_token(token, secret, account=self.with_account)
        self.assertEqual(at.token, token)
        self.assertEqual(at.token_secret, secret)
        self.assertEqual(at.share, pha_share)
        self.assertEqual(at.carenet, None)
        self.assertNotEqual(at.expires_at, None)
        self.assertEqual(at.account, self.with_account)

        # build one for the foreign account to access the app in a carenet
        token, secret = self.generate_token_and_secret()
        at = pha_share.new_access_token(token, secret, account=self.with_account, carenet=self.carenet)
        self.assertEqual(at.token, token)
        self.assertEqual(at.token_secret, secret)
        self.assertEqual(at.share, pha_share)
        self.assertEqual(at.carenet, self.carenet)
        self.assertNotEqual(at.expires_at, None)
        self.assertEqual(at.account, self.with_account)

        # try to build one for the foreign account to access the app in an unrelated carenet
        token, secret = self.generate_token_and_secret()
        self.assertRaises(Exception, pha_share.new_access_token, token, secret, account=self.with_account,
                          carenet=self.with_carenet)

        # build one for the record owner to access the app
        token, secret = self.generate_token_and_secret()
        at = pha_share.new_access_token(token, secret, account=self.account)
        self.assertEqual(at.token, token)
        self.assertEqual(at.token_secret, secret)
        self.assertEqual(at.share, pha_share)
        self.assertEqual(at.carenet, None)
        self.assertNotEqual(at.expires_at, None)
        self.assertEqual(at.account, self.account)

        # build one without an account, as if we were priming the record with the app
        token, secret = self.generate_token_and_secret()
        at = pha_share.new_access_token(token, secret)
        self.assertEqual(at.token, token)
        self.assertEqual(at.token_secret, secret)
        self.assertEqual(at.share, pha_share)
        self.assertEqual(at.carenet, None)
        self.assertNotEqual(at.expires_at, None)
        self.assertEqual(at.account, None)

        # Now share our autonomous app
        pha_share = self.addAppToRecord(self.record, self.a_with_pha)        

        # try to build an access token for a foreign account to access the app
        token, secret = self.generate_token_and_secret()
        self.assertRaises(Exception, pha_share.new_access_token, token, secret, account=self.with_account)

        # Now give the account a full share of the record, and the previous call should work
        self.shareRecordFull(self.record, self.with_account)
        at = pha_share.new_access_token(token, secret, account=self.with_account)
        self.assertEqual(at.token, token)
        self.assertEqual(at.token_secret, secret)
        self.assertEqual(at.share, pha_share)
        self.assertEqual(at.carenet, None)
        self.assertEqual(at.expires_at, None)
        self.assertEqual(at.account, None) # Accounts don't make it into autonomous app Access Tokens

        # try to build an access token for the foreign account to access the app in a carenet
        token, secret = self.generate_token_and_secret()
        self.assertRaises(Exception, pha_share.new_access_token, token, secret, account=self.with_account, 
                          carenet=self.carenet)

        # build one for the record owner to access the app
        token, secret = self.generate_token_and_secret()
        at = pha_share.new_access_token(token, secret, account=self.account)
        self.assertEqual(at.token, token)
        self.assertEqual(at.token_secret, secret)
        self.assertEqual(at.share, pha_share)
        self.assertEqual(at.carenet, None)
        self.assertEqual(at.expires_at, None)
        self.assertEqual(at.account, None) # Accounts don't make it into autonomous app Access Tokens

        # build one without an account, as if we were priming the record with the app
        token, secret = self.generate_token_and_secret()
        at = pha_share.new_access_token(token, secret)
        self.assertEqual(at.token, token)
        self.assertEqual(at.token_secret, secret)
        self.assertEqual(at.share, pha_share)
        self.assertEqual(at.carenet, None)
        self.assertEqual(at.expires_at, None)
        self.assertEqual(at.account, None)

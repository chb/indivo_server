from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.authsystem import TEST_AUTHSYSTEMS
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.models import AccountAuthSystem
from django.db import IntegrityError, transaction

username1 = 'USER1'
username2 = 'UsEr2'
username3 = 'user3'
username4 = 'USER3'

class AccountAuthSystemModelUnitTests(InternalTests):
    def setUp(self):
        super(AccountAuthSystemModelUnitTests, self).setUp()

        # An external auth system
        self.auth_system = self.createAuthSystem(TEST_AUTHSYSTEMS, 0)

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)

        # Another account
        self.account2 = self.createAccount(TEST_ACCOUNTS, 2)

    def tearDown(self):
        super(AccountAuthSystemModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # should construct normally
        args = {'account':self.account,
                'auth_system':self.auth_system,
                'username': username1,
                }
        try:
            aas = AccountAuthSystem.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create AccountAuthSystem normally')
        else:
            sid = transaction.savepoint()
            self.assertEqual(aas, AccountAuthSystem.objects.get(pk=aas.pk))


        # shouldn't be able to add the same authsystem twice to an account
        args['username'] = username2
        try:
              aas = AccountAuthSystem.objects.create(**args)
        except IntegrityError:
            transaction.savepoint_rollback(sid)
        else:
            self.fail('Added the same authsystem twice to the same account')

        # shouldn't be able to have an authsystem with two identical usernames
        args['username'] = username1
        args['account'] = self.account2
        try:
              aas = AccountAuthSystem.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Added two accounts with the same username to a single authsystem')

    @enable_transactions
    def test_lowercase_usernames(self):

        # build an account auth system
        args = {'account':self.account,
                'auth_system':self.auth_system,
                'username': username1,
                }
        aas = AccountAuthSystem.objects.create(**args)
        
        # make sure its username got auto-lowercased
        self.assertEqual(aas.username, username1.lower())

        # make sure this works for mixed-case names
        aas.username = username2
        aas.save()
        self.assertEqual(aas.username, username2.lower())
    
        # should break if we have try to add two equivalent
        # (but differently case) usernames to the same auth system
        aas.username = username3
        aas.save()
        args = {'account': self.account2,
                'auth_system':self.auth_system,
                'username':username4,
                }
        try:
            aas2 = AccountAuthSystem.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Saved two equivalent usernames to the same authsystem')

from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.authsystem import TEST_AUTHSYSTEMS
from indivo.models import AuthSystem
from django.db import IntegrityError, transaction

class AuthSystemModelUnitTests(InternalTests):
    def setUp(self):
        super(AuthSystemModelUnitTests, self).setUp()

    def tearDown(self):
        super(AuthSystemModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # should construct normally
        try:
            auth_system = self.createAuthSystem(TEST_AUTHSYSTEMS, 0)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create AuthSystem normally')
        else:
            sid = transaction.savepoint()
            self.assertEqual(auth_system, AuthSystem.objects.get(pk=auth_system.pk))

        # shouldn't be able to add the same authsystem twice
        try:
            auth_system = self.createAuthSystem(TEST_AUTHSYSTEMS, 0, force_create=True)
        except IntegrityError:
            transaction.savepoint_rollback(sid)
        else:
            self.fail('Added the same authsystem twice')

        # Even if one is internal and the other external
        try:
            auth_system = self.createAuthSystem(TEST_AUTHSYSTEMS, 0, internal_p=True, force_create=True)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Added the same authsystem externally and internally')

    def test_password_authsystem(self):
        
        # System shouldn't exist in the DB by default
        self.assertRaises(AuthSystem.DoesNotExist, AuthSystem.objects.get, short_name='password')
        
        # Should still be able to acces it though, which should create it in the DB
        pw = AuthSystem.PASSWORD()
        self.assertEqual(pw.short_name, 'password')
        self.assertTrue(pw.internal_p)

        # Now it should exist in the DB
        self.assertTrue(AuthSystem.objects.filter(short_name='password').exists())

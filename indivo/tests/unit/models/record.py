from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.message import TEST_MESSAGES
from indivo.models import Record, Carenet, Notification, Message, RecordNotificationRoute
from django.db import IntegrityError, transaction
from django.conf import settings

import copy

class RecordModelUnitTests(InternalTests):
    def setUp(self):
        super(RecordModelUnitTests,self).setUp()
        
        # An Account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # A record for that account
        self.record = self.createRecord(TEST_RECORDS, 1, owner=self.account)

        # An account, full-shared with our record
        self.s_account = self.createAccount(TEST_ACCOUNTS, 2)
        self.shareRecordFull(self.record, self.s_account)

        # An account, shared with nobody
        self.u_account = self.createAccount(TEST_ACCOUNTS, 3)

        # An app, shared with us
        self.app = self.createUserApp(TEST_USERAPPS, 0)
        self.addAppToRecord(self.record, self.app)

        # An app that isn't shared
        self.u_app = self.createUserApp(TEST_USERAPPS, 1)

        # Notification routes for our shared accounts
        self.rnrs = []
        self.rnrs.append(RecordNotificationRoute.objects.create(record=self.record, account=self.account))
        self.rnrs.append(RecordNotificationRoute.objects.create(record=self.record, account=self.s_account))

        # A message we've received
        self.msg = self.createMessage(TEST_MESSAGES, 0, about_record=self.record)

    def tearDown(self):
        super(RecordModelUnitTests,self).tearDown()

    # Not calling self.createRecord here, since that calls record.create_default_carenets, which is
    # transaction-managed. This is why we have to be very careful with the @enable_transactions
    # decorator.
    @enable_transactions
    def test_construction(self):
        
        # should save normally with proper data, external_id or no
        try:
            args = {'label':'empty_record',
                    'owner':self.account,
                    }
            r = Record.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create record with standard args')
        else:
            self.assertEqual(r, Record.objects.get(pk=r.pk))

        try:

            args = {'label':'test_record_extid',
                    'owner':self.account,
                    'external_id':Record.prepare_external_id('RECORD5_EXTID',self.account.email),
                    }
            r = Record.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create record with external id')
        else:
            self.assertEqual(r, Record.objects.get(pk=r.pk))

    def test_prepare_external_id(self):
        local_id = 'TEST_ID'
        principal_email = 'a@b.com'

        self.assertEqual(Record.prepare_external_id(local_id, principal_email), '%s/%s'%(principal_email, local_id))
        self.assertEqual(Record.prepare_external_id(None, principal_email), None)

    def test_can_admin(self):
        self.assertTrue(self.record.can_admin(self.account))
        self.assertTrue(self.record.can_admin(self.s_account))
        self.assertFalse(self.record.can_admin(self.u_account))

    def test_phas(self):
        self.assertEqual(self.record.phas, [self.app])

    def test_has_pha(self):
        self.assertTrue(self.record.has_pha(self.app))
        self.assertFalse(self.record.has_pha(self.u_app))

    def test_get_accounts_to_notify(self):
        self.assertEqual(set(self.record.get_accounts_to_notify()), set([self.account, self.s_account]))

    def test_get_messages(self):
        self.assertEqual(list(self.record.get_messages()), [self.msg])

    def test_send_message(self):
        self.record.send_message('msg_ext_id', self.app, 'subj', 'body', severity='high')

        # Make sure the right people got notified
        for account in [rnr.account for rnr in self.rnrs]:
            self.assertTrue(Message.objects.filter(sender=self.app,
                                                    about_record=self.record, 
                                                    account=account).exists())

        self.assertFalse(Message.objects.filter(sender=self.app, 
                                                about_record=self.record, 
                                                account=self.u_account).exists())
        

    def test_notify(self):
        self.record.notify(self.app, 'Notify This!', app_url=self.app.callback_url)
        
        # and without optional params
        self.record.notify(self.app, 'Notify This Twice!')

        # Make sure the right people got notified
        for account in [rnr.account for rnr in self.rnrs]:
            self.assertEqual(Notification.objects.filter(record=self.record, account=account).count(), 2)

        self.assertEqual(Notification.objects.filter(record=self.record, account=self.u_account).count(), 0)

    def test_create_default_carenets(self):
        
        # Eliminate all of our default carenets
        Carenet.objects.filter(record=self.record).delete()

        self.assertEqual(Carenet.objects.filter(record=self.record).count(), 0)

        # And recreate them
        self.record.create_default_carenets()

        self.assertEqual(Carenet.objects.filter(record=self.record).count(), len(settings.INDIVO_DEFAULT_CARENETS))
        for name in settings.INDIVO_DEFAULT_CARENETS:
            self.assertTrue(Carenet.objects.filter(record=self.record, name=name).exists())

    def test_carenet_alias_id(self):
        self.assertEqual(self.record.carenet_alias_id, self.record.id)

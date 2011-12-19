from indivo.tests.internal_tests import InternalTests
from indivo.models import Notification
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.document import TEST_R_DOCS
from indivo.tests.data.account import TEST_ACCOUNTS

class NotificationModelUnitTests(InternalTests):
    def setUp(self):
        super(NotificationModelUnitTests, self).setUp()
    
        # A recipient account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A sender app
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # A record, owned by the recipient account
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        
        # A document, owned by the record
        self.doc = self.createDocument(TEST_R_DOCS, 0, record=self.record)
                
    def tearDown(self):
        super(NotificationModelUnitTests, self).tearDown()
     
    def test_construction(self):
        args = {
            'account':self.account,
            'sender':self.app,
            'content':'Consider Yourself Notified',
            }
        optional_args = {
            'record':self.record,
            'document':self.doc,
            'app_url':self.app.start_url_template,
            }

        # Should be able to construct normally, with or without optional args
        try:
            n = Notification.objects.create(**args)
        except:
            self.fail('Unable to construct notification without optional args')
        else:
            self.assertEqual(n, Notification.objects.get(pk=n.pk))

        args.update(optional_args)
        try:
            n = Notification.objects.create(**args)
        except:
            self.fail('Unable to construct notification with standard args')
        else:
            self.assertEqual(n, Notification.objects.get(pk=n.pk))

        # Should not be able to construct without a sender or recipient
        try:
            args['sender'] = None
            n = Notification.objects.create(**args)
        except ValueError:
            args['sender'] = self.app
            pass
        else:
            self.fail('Constructed a notification with no sender')

        try:
            args['account'] = None
            n = Notification.objects.create(**args)
        except ValueError:
            pass
        else:
            self.fail('Constructed a notification with no recipient account')

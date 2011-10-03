class RecordTestCase(unittest.TestCase):
    def setUp(self):
        self.account = Account.objects.create(email = 'foo@foo.com')
        self.record = Record.objects.create(owner=self.account, label='Foo Record')

    def tearDown(self):
        self.record.delete()
        self.account.delete()

    def test_send_message(self):
        self.record.send_message("foobar-id", self.account, 'testing message', 'testing message body', body_type='plaintext')

class AccountTestCase(unittest.TestCase):
    def setUp(self):
        self.account = Account.objects.create(email = 'foo@foo.com')

    def tearDown(self):
        self.account.delete()
    
    def test_retired(self):
        self.account.set_state("retired")
        self.assertRaises(Exception, lambda: self.account.set_state("active"))

    def test_password(self):
        self.assertRaises(Exception, lambda: self.account.set_username(username='foobar'))
        self.account.set_username_and_password(username='foobar', password='baz')
        self.account.set_username(username='foobar2')

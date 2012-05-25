from indivo.tests.internal_tests import InternalTests
from indivo.tests.data import TEST_ACCOUNTS, TEST_RECORDS, TEST_USERAPPS

class UserPreferencesIntegrationTests(InternalTests):

    def setUp(self):
        super(UserPreferencesIntegrationTests, self).setUp()

        # Create an Account
        self.account = self.createAccount(TEST_ACCOUNTS, 4)

        # Add a record for it
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        
        # Create an app, and add it to the record
        self.pha = self.createUserApp(TEST_USERAPPS, 0)
        self.addAppToRecord(record=self.record, with_pha=self.pha)

        self.PREFS_URL = '/accounts/%s/apps/%s/preferences'%(self.account.email, self.pha.email)

    def tearDown(self):
        super(UserPreferencesIntegrationTests,self).tearDown()
        
    def test_add_preferences(self):
        
        # Start with no preferences
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '') # No preferences

        # Add some bogus preferences
        prefs = 'MYPREFS'
        response = self.client.put(self.PREFS_URL, data=prefs, content_type='text/plain')
        self.assertEqual(response.status_code, 200)

        # Read them back
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, prefs)

    def test_replace_preferences(self):

        # Add some bogus preferences
        prefs = 'MYPREFS'
        response = self.client.put(self.PREFS_URL, data=prefs, content_type='text/plain')
        self.assertEqual(response.status_code, 200)

        # Read them back
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, prefs)

        # Add some new preferences, XML this time
        new_prefs = "<Preferences>stuff here</Preferences>"
        response = self.client.put(self.PREFS_URL, data=new_prefs, content_type='application/xml')
        self.assertEqual(response.status_code, 200)

        # Read them back: replacement should work
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, new_prefs)

    def test_delete_preferences(self):

        # Start with no preferences
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '') # No preferences

        # Delete them: should succeed with no changes
        response = self.client.delete(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        
        # Still no preferences
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '') # No preferences

        # Add some preferences
        prefs = 'MYPREFS'
        response = self.client.put(self.PREFS_URL, data=prefs, content_type='text/plain')
        self.assertEqual(response.status_code, 200)

        # Read them back
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, prefs)

        # Delete them: should erase the preferences
        response = self.client.delete(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        
        # Should no longer have preferences
        response = self.client.get(self.PREFS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '') # No preferences

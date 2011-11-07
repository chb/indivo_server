from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.document import TEST_R_DOCS, TEST_RA_DOCS, TEST_A_DOCS
from indivo.tests.data.reports import TEST_REPORTS_INVALID, TEST_REPORTS
from indivo.models import Document, StatusName, DocumentStatusHistory, Fact

from django.db import IntegrityError, transaction
from django.conf import settings

import datetime

class DocumentModelUnitTests(InternalTests):
    def setUp(self):
        super(DocumentModelUnitTests, self).setUp()

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0)

        # An app
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # A couple test docs
        self.r_doc1 = self.createDocument(TEST_R_DOCS, 2, record=self.record)
        self.r_doc2 = self.createDocument(TEST_R_DOCS, 10, record=self.record)

    def tearDown(self):
        super(DocumentModelUnitTests, self).tearDown()
        
    @enable_transactions
    def test_construction(self):

        # Should be able to construct record-specific, app-specific,
        # and record-app-specific documents normally
        try:
            r_doc = self.createDocument(TEST_R_DOCS, 6, record=self.record)
            ra_doc = self.createDocument(TEST_RA_DOCS, 0, record=self.record)
            a_doc = self.createDocument(TEST_A_DOCS, 0, record=self.record)
        except IntegrityError:
            transaction.rollback()
            self.fail('Unable to construct documents with standard arguments')
        else:
            self.assertEqual(r_doc, Document.objects.get(pk=r_doc.pk))
            self.assertEqual(ra_doc, Document.objects.get(pk=ra_doc.pk))
            self.assertEqual(a_doc, Document.objects.get(pk=a_doc.pk))

        # Should be able to do the same with external ids
        try:
            re_doc = self.createDocument(TEST_R_DOCS, 0, record=self.record)
            rae_doc = self.createDocument(TEST_RA_DOCS, 1, record=self.record)
            ae_doc = self.createDocument(TEST_A_DOCS, 1, record=self.record)
        except IntegrityError:
            transaction.rollback()
            self.fail('Unable to construct documents with standard arguments and external_ids')
        else:
            self.assertEqual(re_doc, Document.objects.get(pk=re_doc.pk))
            self.assertEqual(rae_doc, Document.objects.get(pk=rae_doc.pk))
            self.assertEqual(ae_doc, Document.objects.get(pk=ae_doc.pk))

        # And with a binary payload
        try:
            b_doc = self.createDocument(TEST_R_DOCS, 1, record=self.record, mime_type='application/pdf')
        except IntegrityError:
            transaction.rollback()
            self.fail('Unable to construct binary document')
        else:
            self.assertEqual(b_doc, Document.objects.get(pk=b_doc.pk))
            self.assertEqual(b_doc.content, None)
            self.assertNotEqual(b_doc.content_file.name, None) # If name isn't none, then the file has been saved

        # But no two docs can have the same record and external id
        try:
            re_doc2 = self.createDocument(TEST_R_DOCS, 0, record=self.record, force_create=True)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Created 2 docs with the same record and external id')

    def test_prepare_external_id(self):
        valid_args = {('abc', self.app, False, True): '%s/%s'%(self.app.email, 'abc'),
                      ('bcd', self.app, True, True): '%s/INTERNAL/%s'%(self.app.email, 'bcd'),
                      ('cde', self.app, True, False): '%s/NORECORD/%s'%(self.app.email, 'cde'),
                      }
        
        invalid_args = {('def', None): ValueError,
                        ('efg', self.app, False, False): ValueError,
                        }

        # Make sure ids are generated properly
        for args, correct_id in valid_args.iteritems():
            self.assertEqual(Document.prepare_external_id(*args), correct_id)

        # Make sure invalid args throw errors
        for args, error in invalid_args.iteritems():
            self.assertRaises(error, Document.prepare_external_id, *args)

    def test_set_latest_info(self):
        # None of the latest attributes should be set 
        # (these are set only in memory when the doc is returned)
        self.assertFalse(hasattr(self.r_doc1, 'latest_id'))
        self.assertFalse(hasattr(self.r_doc1, 'latest_created_at'))
        self.assertFalse(hasattr(self.r_doc1, 'latest_creator_email'))

        # Set the info, assuming that we are the latest doc
        self.r_doc1.latest(self.r_doc1.id, self.r_doc1.created_at, self.r_doc1.creator.email)

        # All of the latest attributes should be set 
        self.assertTrue(hasattr(self.r_doc1, 'latest_id'))
        self.assertTrue(hasattr(self.r_doc1, 'latest_created_at'))
        self.assertTrue(hasattr(self.r_doc1, 'latest_creator_email'))
        self.assertEqual(self.r_doc1.latest_id, self.r_doc1.id)
        self.assertEqual(self.r_doc1.latest_created_at, self.r_doc1.created_at)
        self.assertEqual(self.r_doc1.latest_creator_email, self.r_doc1.creator.email)

        # Set the info, assuming that we've been replaced.
        self.r_doc1.latest(self.r_doc2.id, self.r_doc2.created_at, self.r_doc2.creator.email)

        # All of the latest attributes should be set 
        self.assertTrue(hasattr(self.r_doc1, 'latest_id'))
        self.assertTrue(hasattr(self.r_doc1, 'latest_created_at'))
        self.assertTrue(hasattr(self.r_doc1, 'latest_creator_email'))
        self.assertEqual(self.r_doc1.latest_id, self.r_doc2.id)
        self.assertEqual(self.r_doc1.latest_created_at, self.r_doc2.created_at)
        self.assertEqual(self.r_doc1.latest_creator_email, self.r_doc2.creator.email)


    def test_set_status(self):
        principal = self.account
        good_statuses = ['void', 'archived', 'active']
        bad_status = 'CRAZYSTATUS'
        reason = 'because I am awesome, and I want the doc status to be %s'

        status_objs = dict([(s.name, s) for s in StatusName.objects.all().iterator()])
        
        # status should start out active
        self.assertEqual(self.r_doc1.status, status_objs['active'])

        # change the status and make sure that everything is working
        for status in good_statuses:
            self.r_doc1.set_status(principal, status, reason%status)
            self.assertEqual(self.r_doc1.status, status_objs[status])
            
            try:
                dsh = DocumentStatusHistory.objects.get(document = self.r_doc1.id,
                                                        status = status_objs[status])
                self.assertEqual(dsh.record, self.r_doc1.record.id)
                self.assertEqual(dsh.status, self.r_doc1.status)
                self.assertEqual(dsh.reason, reason%status)
                self.assertEqual(dsh.proxied_by_principal, None)
                self.assertEqual(dsh.effective_principal, self.account.email)
            except DocumentStatusHistory.DoesNotExist:
                self.fail('DocumentStatusHistory object was not created properly')

        # Invalid status should fail
        self.assertRaises(StatusName.DoesNotExist, self.r_doc2.set_status, principal, bad_status, reason%bad_status)

        # And should not create status histories
        self.assertFalse(DocumentStatusHistory.objects.filter(document=self.r_doc2.id).exists())

    def test_replace(self):
        new_content = self.r_doc2.content
        new_mimetype = 'text/xml'
        new_digest = self.r_doc2.digest
        new_size = self.r_doc2.size
        new_type = self.r_doc2.type

        # Make sure we start out with the appropriate state
        self.assertNotEqual(self.r_doc1.content, new_content)
        self.assertNotEqual(self.r_doc1.mime_type, new_mimetype)
        self.assertNotEqual(self.r_doc1.digest, new_digest)
        self.assertNotEqual(self.r_doc1.size, new_size)
        self.assertNotEqual(self.r_doc1.type, new_type) # This is broken right now, need to fix doc typing

        # Replace the doc, make sure it worked
        self.r_doc1.replace(new_content, new_mimetype)
        self.assertEqual(self.r_doc1.content, new_content)
        self.assertEqual(self.r_doc1.mime_type, new_mimetype)
        self.assertEqual(self.r_doc1.digest, new_digest)
        self.assertEqual(self.r_doc1.size, new_size)
        self.assertEqual(self.r_doc1.type, new_type)

        # Replace the doc with bad XML, make sure it fails if validation is on
        malformed_xml = '<AwesomeTag>Stuff<WrongTag>'
        invalid_xml = TEST_REPORTS_INVALID[1]['content']

        settings.VALIDATE_XML_SYNTAX = True
        self.assertRaises(ValueError, self.r_doc1.replace, malformed_xml, new_mimetype)
        settings.VALIDATE_XML_SYNTAX = False
        try:
            self.r_doc1.replace(malformed_xml, new_mimetype)
        except ValueError:
            self.fail('Could not add malformed document even with validation off')

        settings.VALIDATE_XML = True
        self.assertRaises(ValueError, self.r_doc1.replace, invalid_xml, new_mimetype)
        settings.VALIDATE_XML = False
        try:
            self.r_doc1.replace(invalid_xml, new_mimetype)
        except ValueError:
            self.fail('Could not add invalid document even with validation off')

        # Set the doc to replaced, make sure replacing it fails
        self.r_doc1.replaced_by = self.r_doc2
        self.assertRaises(ValueError, self.r_doc1.replace, new_content, new_mimetype)

    def test_save(self):

        # Number of existing fobjs, as reference
        n_fobjs = Fact.objects.all().count()

        # Make sure saving an invalid doc throws an error and doesn't produce any f_objs
        malformed_xml = '<Allergy>Stuff<WrongTag>'
        invalid_xml = TEST_REPORTS_INVALID[1]['content']
        self.r_doc1.processed=False

        self.r_doc1.content = malformed_xml
        settings.VALIDATE_XML_SYNTAX = True
        self.assertRaises(ValueError, self.r_doc1.save)
        self.assertEqual(n_fobjs, Fact.objects.all().count())
        self.assertFalse(self.r_doc1.processed)

        self.r_doc1.content = invalid_xml
        settings.VALIDATE_XML = True
        self.assertRaises(ValueError, self.r_doc1.save)
        self.assertEqual(n_fobjs, Fact.objects.all().count())
        self.assertFalse(self.r_doc1.processed)
        settings.VALIDATE_XML = False
        try:
            self.r_doc1.save()
        except ValueError:
            self.fail('Could not process/save an invalid document, even with validation off')
        old_n_fobjs = n_fobjs
        n_fobjs = Fact.objects.all().count()
        self.assertNotEqual(old_n_fobjs, n_fobjs) # should have created an f_obj, even though invalid
        self.assertTrue(self.r_doc1.processed) # should have successfully processed, even though invalid

        # Make sure saving a valid doc works.
        self.r_doc1.content = TEST_REPORTS[0]['content']
        self.r_doc1.processed = False
        self.r_doc1.save()
        old_n_fobjs = n_fobjs
        n_fobjs = Fact.objects.all().count()
        self.assertNotEqual(old_n_fobjs, n_fobjs)
        self.assertTrue(self.r_doc1.processed)

        # Make sure re-saving a valid doc doesn't re-process it
        self.r_doc1.save()
        self.assertEqual(n_fobjs, Fact.objects.all().count())
        self.assertTrue(self.r_doc1.processed)

        # Make sure saving a doc that doesn't match our schemas works
        self.r_doc1.content = TEST_R_DOCS[2]['content']
        self.r_doc1.processed = False
        self.r_doc1.save()
        self.assertTrue(self.r_doc1.processed)
        self.assertEqual(n_fobjs, Fact.objects.all().count())

        # Make sure setting the external_id on this doc worked
        self.assertEqual(self.r_doc1.external_id, Document.objects.get(id=self.r_doc1.id).external_id)
        
        # Make sure it works on a doc without and external_id
        self.r_doc1.external_id = None
        self.r_doc1.save()
        self.assertEqual(self.r_doc1.external_id, self.r_doc1.id)

        # Make sure self.original has been set
        self.assertEqual(self.r_doc1.original, self.r_doc1)

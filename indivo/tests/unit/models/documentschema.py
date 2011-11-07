from indivo.tests.internal_tests import InternalTests
from indivo.models import DocumentSchema

from django.db import IntegrityError, transaction

class DocumentSchemaModelUnitTests(InternalTests):
    def setUp(self):
        super(DocumentSchemaModelUnitTests, self).setUp()

        # An existing schema
        self.schema = DocumentSchema.objects.get(type=DocumentSchema.expand_rel('annotation'))

        self.internal_schema_name = 'new_internal_schema'
        self.external_schema_name = 'http://mysweetdomain.com/schemas#new_external_schema'

    def tearDown(self):
        super(DocumentSchemaModelUnitTests, self).tearDown()
        
    def test_construction(self):

        # Should be able to construct normally
        # Note: not testing the stylesheet attribute because this is highly broken
        try:
            ds = DocumentSchema(type=self.internal_schema_name, stylesheet=None, internal_p=False)
        except:
            self.fail('Unable to construct documentschema with standard arguments')

    def test_expand_rel(self):
        
        # should work on namespaced and internal rels
        self.assertEqual(DocumentSchema.expand_rel(self.internal_schema_name),
                         '%s%s'%(DocumentSchema.DEFAULT_REL_NAMESPACE, self.internal_schema_name))

        self.assertEqual(DocumentSchema.expand_rel(self.external_schema_name), self.external_schema_name)

    def test_uri(self):

        # Should always match type
        self.assertEqual(self.schema.uri, self.schema.type)

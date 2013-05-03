from django.utils import timezone

from indivo.tests.internal_tests import InternalTests
from indivo.models import Audit


class AuditModelUnitTests(InternalTests):
    def setUp(self):
        super(AuditModelUnitTests, self).setUp()

    def tearDown(self):
        super(AuditModelUnitTests, self).tearDown()

    def test_construction(self):
        now = timezone.now()
        
        args = {'datetime':now,
                'view_func':'create_record',
                'request_successful':True,
                'effective_principal_email':'drawesome@indivo.org',
                'proxied_by_email':'app1@indivo.org',
                'carenet_id':'abcdefg',
                'record_id':'abcdef',
                'pha_id':'app1@indivo.org',
                'document_id':'abcdef',
                'external_id':'EXTERNAL',
                'message_id':'abcdef',
                'req_url':'/records/',
                'req_ip_address':'1.0.0.0',
                'req_domain':'hi.com',
                'req_headers':'abcd',
                'req_method':'POST',
                'resp_code':200,
                'resp_headers':'abcd',
                }

        minimal_args = {'datetime':now,
                        'request_successful':True,
                        }

        # Should construct normally
        a = Audit.objects.create(**args)
        self.assertEqual(a, Audit.objects.get(pk=a.pk))

        # Should construct normally with minimal args
        a = Audit.objects.create(**minimal_args)
        self.assertEqual(a, Audit.objects.get(pk=a.pk))

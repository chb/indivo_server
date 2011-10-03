class CarenetTestCase(unittest.TestCase):
    def setUp(self):
        self.record = Record.objects.create()
        self.status = StatusName.objects.create(name='active')
        self.contact = Document.objects.create(record = self.record, content= CONTACT, size=len(CONTACT), status = self.status)
        self.record.contact = self.contact
        self.record.save()

        self.record.create_default_carenets()
        self.carenet = self.record.carenet_set.all()[0]

    def test_add_doc(self):
        self.carenet.add_doc(self.record.contact)
        assert(self.carenet.contains_doc(self.record.contact))
        assert(self.carenet.contact)

        self.carenet.remove_doc(self.record.contact)
        assert(not self.carenet.contact)
        assert(not self.carenet.contains_doc(self.record.contact))

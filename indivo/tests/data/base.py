import hashlib

class TestXMLDoc(object):
    def __init__(self, xml, label='testing'):
        self.xml = xml
        self._len = None
        self._digest = None
        self.label = label

    def size(self):
        if not self._len:
            self._len = len(self.xml)
        return self._len

    def digest(self):
        if not self._digest:
            md = hashlib.sha256()
            md.update(self.xml)
            self._digest = md.hexdigest()
        return self._digest

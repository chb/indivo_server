from indivo.models import Document

class DocumentUtils:

  def get_latest_doc(self, docid):
    docobj = Document.objects.get(id=docid)

    try:
      latest = Document.objects.get(original=docobj.original,
                                    replaced_by=None)
    except Document.DoesNotExist:
      raise ValueError("No objects exist with original document of passed document, db is in a corrupted state")
    except Document.MultipleObjectsReturned:
      raise ValueError("More than one 'latest' document, db is in a corrupted state")
    
    return latest

  def is_binary(self, data):
    NULL_CHR = '#'
    count, null_count  = 1.0, 0.0 
    threshold = 0.20
    if isinstance(data, str) or isinstance(data, unicode):
      printable = ''.join(["%s" % ((  ord(x) <= 127 and \
                                      len(repr(chr(ord(x))))  == 3 and \
                                      chr(ord(x))) or \
                                    NULL_CHR) 
                                for x in data])
      for char in printable:
        if char == NULL_CHR:
          null_count += 1
        count += 1
      if null_count / count  > threshold:
        return True
    return False


"""
.. module: lib.sample_data
   :synopsis: Libary functions for loading sample data into Indivo records.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

from django.conf import settings
from django.db import transaction
import os
import glob

SUPPORTED_DOCUMENT_TYPES = {
    '.xml': 'application/xml',
    '.pdf': 'application/pdf',
    '.png': 'image/png',
    '.bmp': 'image/bmp',
    '.gif': 'image/gif',
    '.jpg': 'image/jpeg',
    '.zip': 'application/x-zip',
    '.tar': 'application/x-tar',
    '.gz': 'application/x-gzip',
    '.bz2': 'application/x-bz2',
}

class IndivoDataLoader(object):
    def __init__(self, loader_principal, data_dir=settings.SAMPLE_DATA_DIR):
        from indivo.views.documents.document import _document_create
        self._document_create = _document_create
        self.creator = loader_principal
        self.data_dir = data_dir

    @transaction.commit_manually
    def load_profile(self, record, profile):
        """ Bulk load data into a record.
    
        Loads every document identified by *profile* into *record*.
        
        **Arguments:**
    
        * *creator*: The :py:class:`~indivo.models.base.Principal` instance responsible for
          creating the documents.
    
        * *record*: The :py:class:`~indivo.models.records_and_documents.Record` instance to
          which to assign new documents

        * *profile*: The data profile to load into the record. This is a string, and should
          correspond to a subdirectory of *data_dir*

        * *data_dir*: The directory in which data can be found. The format of this directory
          should look like::

            profile_1/  # Data profiles. Each directory should correspond to a single patient.
            profile_2/
               ...
            profile_n/
              Contact.xml # An optional contact document.
              Demographics.xml # An optional demographics document.

              doc_1.xml # XML Data to load goes here.
              doc_2.xml # File names MUST be prefixed with 'doc_'.
                 ...
              doc_n.xml

              doc_1.pdf # Other extensions are treated as binary docs.
              doc_2.pdf # Also prefix names with 'doc_'.
                 ...

        **Returns:**
    
        * ``None``, on success.

        **Raises:**
        
        * :py:exc:`ValueError` if *profile* doesn't correspond to an existing data profile

        """

        # quick security check
        if profile.startswith('.') or profile.startswith('/'):
            raise ValueError("invalid data profile")

        docs_dir = os.path.join(self.data_dir, profile)
        if not os.path.exists(docs_dir):
            raise ValueError("invalid data profile")

        # Transactional: rolled back on failure
        try:

            # load in the special docs
            self.load_special_docs(docs_dir, record)
    
            # load in the rest of the docs
            for raw_content, mime_type in self.get_all_docs(docs_dir):
                self._document_create(self.creator, raw_content, pha=None,
                                      record=record, mime_type=mime_type)
        except Exception, e:
            transaction.rollback()
            raise
        else:
            transaction.commit()

    def get_all_docs(self, data_dir):
        return self._yield_docs(glob.iglob(os.path.join(data_dir, 'doc_*')))

    def _yield_docs(self, filepaths, open_mode='r'):
        for path in filepaths:
            mime_type = SUPPORTED_DOCUMENT_TYPES.get(os.path.splitext(path)[1], None)
            if not mime_type:
                continue # unrecognized doc type: skipping

            with open(path, open_mode) as f:
                data = f.read()
            yield (data, mime_type)

    def load_special_docs(self, data_dir, record, save=True):
        """ Load the special docs in *data_dir* into *record*. """

        contact_raw = self._get_named_doc(data_dir, 'Contact.xml')
        demographics_raw = self._get_named_doc(data_dir, 'Demographics.xml')
        
        if contact_raw:
            contact_doc = self._document_create(self.creator, contact_raw, 
                                                pha=None, record=record)
            record.contact = contact_doc
        
        if demographics_raw:
            demographics_doc = self._document_create(self.creator, demographics_raw, 
                                                     pha=None, record=record)
            record.demographics = demographics_doc
        
        if save:
            record.save()


    def _get_named_doc(self, data_dir, name):
        """ Return the raw content of a document with a specific name from a data profile.
    
        Returns none if a file named *name* doesn't exist in *data_dir*

        """
    
        full_path = os.path.join(data_dir, name)
        if not os.path.exists(full_path):
            return None
    
        with open(full_path, 'r') as f:
            data = f.read()
            
        return data
    

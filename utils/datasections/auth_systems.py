from indivo import models
import importer_utils

class Auth_systems:

  def __init__(self, elements, verbosity):
    kwargs = []
    for node in elements.childNodes:
      kwarg = {}
      kwarg['short_name'] = node.getAttribute('short_name')
      kwarg['internal_p'] = importer_utils.clean_value(node.getAttribute('internal_p'))
      kwargs.append(kwarg)
      if verbosity:
        print "\tAdding authsystem: ", node.getAttribute('short_name')
    for kw in kwargs:
      models.AuthSystem.objects.get_or_create(**kw)

from indivo import models

class Status_names:
  def __init__(self, elements, verbosity):
    kwargs = []
    for node in elements.childNodes:
      kwarg = {}
      kwarg['id'] = node.getAttribute('id')
      kwarg['name'] = node.getAttribute('name')
      kwargs.append(kwarg)
    for kw in kwargs:
      models.StatusName.objects.get_or_create(**kw)

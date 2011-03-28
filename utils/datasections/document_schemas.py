from indivo import models

class Document_schemas:
  def __init__(self, nodes, verbosity):
    kwargs = []
    for node in nodes.childNodes:
      kwarg = {}
      kwarg['type'] = node.getAttribute('type')
      kwargs.append(kwarg)
    for kw in kwargs:
      models.DocumentSchema.objects.get_or_create(**kw)

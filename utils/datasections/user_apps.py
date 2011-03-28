from indivo import models
import importer_utils

class User_apps:
  userapp_tags = ('name',         'email', 'consumer_key', 'secret', 'has_ui', 
                  'frameable',    'is_autonomous', 'autonomous_reason',
                  'start_url_template', 'callback_url', 
                  'description',  'document_schema')

  def __init__(self, userapps_node, verbosity):
    self.process_userapps(userapps_node, verbosity)

  def process_userapps(self, userapps_node, verbosity):
    user_apps = []
    for node in userapps_node.childNodes:
      user_app = {}
      user_app_name = node.getAttribute(self.userapp_tags[0])
      user_app[self.userapp_tags[0]] = user_app_name
      user_app[self.userapp_tags[1]] = node.getAttribute(self.userapp_tags[1])
      if verbosity:
        print "\tAdding app: ", user_app_name
      for tag_name in self.userapp_tags:
        elem_node = node.getElementsByTagName(tag_name)
        if elem_node and len(elem_node) > 0:
          if elem_node[0].firstChild:
            user_app[tag_name] = importer_utils.clean_value(elem_node[0].firstChild.nodeValue)
          else:
            user_app[self.userapp_tags[-1]] =  elem_node[0].getAttribute('type')
      user_apps.append(user_app)
    return self.create_userapps(user_apps)

  def create_userapps(self, user_apps):
    for ua in user_apps:
      if self.userapp_tags[-1] in ua: 
        try:
          ua['schema'] = models.DocumentSchema.objects.get(type=ua[self.userapp_tags[-1]])
        except models.DocumentSchema.DoesNotExist:
          pass
        del ua[self.userapp_tags[-1]]
      models.PHA.objects.get_or_create(**ua)
    return True

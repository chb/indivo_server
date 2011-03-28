from indivo import models
import importer_utils

class Machine_apps:
  machineapp_tags = ('name', 'email', 'consumer_key', 'secret', 'app_type')

  def __init__(self, machineapps_node, verbosity):
    self.process_machineapps(machineapps_node, verbosity)

  def process_machineapps(self, machineapps_node, verbosity):
    machine_apps = []
    for node in machineapps_node.childNodes:
      machine_app = {}
      machine_app_name = node.getAttribute(self.machineapp_tags[0])
      machine_app[self.machineapp_tags[0]] = machine_app_name
      machine_app[self.machineapp_tags[1]] = node.getAttribute(self.machineapp_tags[1])
      if verbosity:
        print "\tAdding admin app: ", machine_app_name
      for tag_name in self.machineapp_tags:
        elem_node = node.getElementsByTagName(tag_name)
        if elem_node and len(elem_node) > 0 and elem_node[0].firstChild:
          machine_app[tag_name] = importer_utils.clean_value(elem_node[0].firstChild.nodeValue)
      machine_apps.append(machine_app)
    return self.create_machineapps(machine_apps)

  def create_machineapps(self, machine_apps):
    for machine_app in machine_apps:
      models.MachineApp.objects.get_or_create(**machine_app)
    return True

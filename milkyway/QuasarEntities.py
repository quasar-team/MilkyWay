import logging
import opcua

class QuasarClass():
    """Represents a QuasarClass"""
    def __init__(self, objectified_class, milkyway_server):
        # TODO: need objectified class ?
        # should we have a ref to milkyway server
        self.milkyway_server = milkyway_server
        self._objectified_class = objectified_class
        self.name = objectified_class.attrib['name']

    def _instantiate_type(self, ua_server: opcua.Server, ns_index):
        types_node = ua_server.get_node(opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectTypesFolder))
        types_node.add_object_type(ns_index, self.name) # TODO: wrong address!

    def instantiate_object(self, ua_server: opcua.Server, parent_nodeid: opcua.ua.uatypes.NodeId, name, ns_index):
        logging.error(f'Instantiating quasar class {self.name}: begin')
        object_nodeid = ua_server.get_node(parent_nodeid).add_object (ns_index, name)
        initial_value = "Acs"
        object_node = ua_server.get_node(object_nodeid)
        object_node.add_variable(ns_index, "Variable", initial_value)
        self._instantiate_cache_variables(ua_server, object_node)
        logging.error(f'Instantiating quasar class: end')

    def _instantiate_cache_variables(self, ua_server: opcua.Server, object_node):
        for cv in self._objectified_class.cachevariable:
            print(cv.attrib['name'])
            initial_value = None
            object_node.add_variable(1, cv.attrib['name'], initial_value)

import logging
import opcua

class QuasarClass():
    """Represents a QuasarClass"""
    def __init__(self, objectified_class, ua_server):
        self.ua_server = ua_server
        self._objectified_class = objectified_class
        self.name = objectified_class.attrib['name']

    def _instantiate_type(self, server):
        types_node = server.get_node(opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectTypesFolder))
        types_node.add_object_type(1, self.name)

    def instantiate_object(self, parent_nodeid, name):
        logging.error(f'Instantiating quasar class {self.name}: begin')
        if parent_nodeid == '.':
            parent_nodeid = opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectsFolder)
        else:
            raise NotImplementedError()
        self.ua_server.get_node(parent_nodeid).add_object (1, name)
        logging.error(f'Instantiating quasar class: end')

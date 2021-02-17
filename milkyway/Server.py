import opcua
from opcua import ua
import time
from milkyway.DesignInspector import DesignInspector
import logging

class QuasarClass():
    """Represents a QuasarClass"""
    def __init__(self, objectified_class):
        self._objectified_class = objectified_class
        self.name = objectified_class.attrib['name']

    def _instantiate_type(self, server):
        types_node = server.get_node(ua.NodeId(opcua.ua.ObjectIds.TypesFolder))
        types_node.add_object_type(1, self.name)

class Server():
    def __init__(self, quasar_design_path):
        self.design_inspector = DesignInspector(quasar_design_path)
        self._load_quasar_classes()

    def _load_quasar_classes(self):
        logging.error('Loading quasar classes: begin')
        self._quasar_classes = {}
        for klass in self.design_inspector.get_names_of_all_classes():
            objectified_class = self.design_inspector.objectify_class(klass)
            quasar_class = QuasarClass(objectified_class)
            self._quasar_classes[klass] = quasar_class
        logging.error(f'Loading quasar classes: end, loaded {len(self._quasar_classes)}')

    def create_object(self, klass, parent_nodeid):
        class_o = self.design_inspector.objectify_class(klass)
        print(class_o)

    def run(self):
        """Runs this server"""
        server = opcua.Server()
        server.set_endpoint("opc.tcp://0.0.0.0:4841")

        objects = server.get_objects_node()

        # import pdb; pdb.set_trace()

        for quasar_class in self._quasar_classes.values():
            quasar_class._instantiate_type(server)

        server.start()



        try:
            time.sleep(1E6)
        except KeyboardInterrupt:
            print("Received Ctrl-C, exiting")
        server.stop()

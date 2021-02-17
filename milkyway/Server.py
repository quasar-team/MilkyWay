import opcua
import time
from milkyway.DesignInspector import DesignInspector

class QuasarClass():
    """Represents a QuasarClass"""
    pass

class Server():
    def __init__(self, quasar_design_path):
        self.design_inspector = DesignInspector(quasar_design_path)

    def create_object(self, klass, parent_nodeid):
        class_o = self.design_inspector.objectify_class(klass)
        print(class_o)

    def run(self):
        """Runs this server"""
        server = opcua.Server()
        server.set_endpoint("opc.tcp://0.0.0.0:4841")

        objects = server.get_objects_node()

        for klass in self.design_inspector.get_names_of_all_classes():
            objects.add_object_type(1, klass)

        # import pdb; pdb.set_trace()


        server.start()



        try:
            time.sleep(1E6)
        except KeyboardInterrupt:
            print("Received Ctrl-C, exiting")
        server.stop()

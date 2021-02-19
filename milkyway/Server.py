import opcua
from opcua import ua
import time
from milkyway.DesignInspector import DesignInspector
from milkyway.QuasarEntities import QuasarClass
import logging



class Server():
    def __init__(self, quasar_design_path):
        self.design_inspector = DesignInspector(quasar_design_path)
        self.initialize()

    def _load_quasar_classes(self):
        """Loads quasar classes from Design into internal storage"""

        logging.error('Loading quasar classes: begin')
        self._quasar_classes = {}
        for klass in self.design_inspector.get_names_of_all_classes():
            objectified_class = self.design_inspector.objectify_class(klass)
            quasar_class = QuasarClass(objectified_class, self.ua_server)
            self._quasar_classes[klass] = quasar_class
        logging.error(f'Loading quasar classes: end, loaded {len(self._quasar_classes)}')

    def initialize(self):
        """Creates FreeOPCUA server structure, populates types."""

        self.ua_server = opcua.Server()
        self.ua_server.set_endpoint("opc.tcp://0.0.0.0:4841")
        self.ua_server.register_namespace('urn:QuasarNameSpace')

        self._load_quasar_classes()
        for quasar_class in self._quasar_classes.values():
            quasar_class._instantiate_type(self.ua_server)



    def run(self):
        """Runs this server, i.e. start handling OPCUA requests"""


        self.ua_server.start()


        try:
            time.sleep(1E6)
        except KeyboardInterrupt:
            print("Received Ctrl-C, exiting")
        self.ua_server.stop()

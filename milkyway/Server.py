import opcua
from opcua import ua
import time
from milkyway.DesignInspector import DesignInspector
from milkyway.QuasarEntities import QuasarClass
import logging
from lxml import etree
import pdb

class Server():
    def __init__(self, quasar_design_path):
        etree.register_namespace('c', 'http://cern.ch/quasar/Configuration')
        self.design_inspector = DesignInspector(quasar_design_path)
        self.initialize()

    def _load_quasar_classes(self):
        """Loads quasar classes from Design into internal storage"""

        logging.error('Loading quasar classes: begin')
        self._quasar_classes = {}
        for klass in self.design_inspector.get_names_of_all_classes():
            objectified_class = self.design_inspector.objectify_class(klass)
            quasar_class = QuasarClass(objectified_class, self)
            self._quasar_classes[klass] = quasar_class
        logging.error(f'Loading quasar classes: end, loaded {len(self._quasar_classes)}')

    def initialize(self):
        """Creates FreeOPCUA server structure, populates types."""

        self.ua_server = opcua.Server()
        self.ua_server.set_endpoint("opc.tcp://0.0.0.0:4841")
        self.quasar_nsi = self.ua_server.register_namespace('urn:QuasarNameSpace')

        self._load_quasar_classes()
        for quasar_class in self._quasar_classes.values():
            quasar_class._instantiate_type(self.ua_server, self.quasar_nsi)

    def recursive_instantiation(self, parent_element, parent_nodeid):
        for child in parent_element:
            if type(child) != etree._Element:
                continue
            klass = child.tag.replace('{http://cern.ch/quasar/Configuration}', '')
            if klass in ['StandardMetaData', 'CalculatedVariable']:
                continue # maybe a nice warning?
            try:
                quasar_class = self._quasar_classes[klass]
                new_object = quasar_class.instantiate_object(self.ua_server, parent_nodeid, child.attrib['name'], self.quasar_nsi)
                self.recursive_instantiation(child, new_object.nodeid)
            except KeyError as ex:
                print(f'Exception caught: {ex}')

    def instantiate_from_config(self, config_file):
        config_file = open(config_file, 'r', encoding='utf-8')
        tree = etree.parse(config_file)

        root = tree.getroot()
        self.recursive_instantiation(root, opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectsFolder))

        # for child in root.getchildren():
        #     if child.tag == '{http://cern.ch/quasar/Configuration}StandardMetaData':
        #         print('WRN: reading of StandardMetaData not yet supported!')
        #         continue
        #     klass = child.tag.replace('{http://cern.ch/quasar/Configuration}', '')
        #     # do we have this class?
        #     quasar_class = self._quasar_classes[klass]
        #     new_object = quasar_class.instantiate_object(self.ua_server, '.', child.attrib['name'], self.quasar_nsi)


        # which quasar classes are at the root?
        has_objs = self.design_inspector.objectify_any("/d:design/d:root/d:hasobjects[@instantiateUsing='configuration']")
        for has_obj in has_objs:
            klass = has_obj.attrib['class']
            print(klass)

        print('Note: config instantiation not yet done!')
        pass


    def start(self, wait_for_stop=False):
        """Runs this server, i.e. start handling OPCUA requests"""

        self.ua_server.start()
        if wait_for_stop:
            self.wait_for_stop()
            self.stop()

    def stop(self):
        self.ua_server.stop()

    def wait_for_stop(self):
        while True:
            try:
                time.sleep(1E6)
            except KeyboardInterrupt:
                print("Received Ctrl-C, exiting")
                return

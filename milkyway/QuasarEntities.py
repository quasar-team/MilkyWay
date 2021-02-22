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
        self._instantiate_methods(ua_server, object_node)
        quasar_object = QuasarObject(self)
        quasar_object._instantiate_cache_variables(ua_server, object_node)
        logging.error(f'Instantiating quasar class: end')
        return quasar_object

    def _instantiate_methods(self, ua_server: opcua.Server, object_node):
        for method in self._objectified_class.method:
            print(f"Method: {method.attrib['name']}")
            object_node.add_method(1, method.attrib['name'], None)

class QuasarObject():
    """Represents an OPCUA object created with milkyway"""

    def __init__(self, quasar_class: QuasarClass):
        self.quasar_class = quasar_class
        self.cache_variables = {}
        self.methods = {}
        self.cache_variables_setters = {}

    def set_cv(self, cv_name, value, status=None, source_time=None):
        if not cv_name in self.cache_variables:
            raise IndexError(f'No such cache-variable {cv_name} in quasar class {self.quasar_class.name}')
        
        self.cache_variables[cv_name].set_value(value)



    def _instantiate_cache_variables(self, ua_server: opcua.Server, object_node):
        for cv in self.quasar_class._objectified_class.cachevariable:
            print(cv.attrib['name'])
            initial_value = None
            var_node_id = object_node.add_variable(1, cv.attrib['name'], initial_value)
            var_node = ua_server.get_node(var_node_id)
            self.cache_variables[cv.attrib['name']] = var_node
            setter_name = f"set{cv.attrib['name'].title()}"
            self.cache_variables_setters[setter_name] = cv.attrib['name']

    def __getattr__(self, name):
        print(f'getattr on {name}')
        # in case:
        if name in self.cache_variables_setters:
            return lambda *args: self.set_cv(self.cache_variables_setters[name], args[0])
        return super(QuasarObject, self).__getattribute__(name)

    def __call__(self, *args):
        print(f'name= args={args}')

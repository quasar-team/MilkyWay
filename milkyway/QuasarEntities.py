import logging
import opcua
from opcua.ua import VariantType
import pdb

class MilkyWayOracle():
    DataTypeToVariantType = {
        'OpcUa_Double'  : VariantType.Int32,
        'OpcUa_Float'   : 'toFloat',
        'OpcUa_Byte'    : 'toByte',
        'OpcUa_SByte'   : 'toSByte',
        'OpcUa_Int16'   : 'toInt16',
        'OpcUa_UInt16'  : 'toUInt16',
        'OpcUa_Int32'   : VariantType.Int32,
        'OpcUa_UInt32'  : 'toUInt32',
        'OpcUa_Int64'   : 'toInt64',
        'OpcUa_UInt64'  : 'toUInt64',
        'OpcUa_Boolean' : 'toBool',
        'UaByteString'  : 'toByteString'
    }

    QuasarDataTypeToDataType = {
        'OpcUa_Double'  : opcua.ua.NodeId(11)
    }

    def quasar_data_type_to_node_id(quasar_data_type):
        try:
            return MilkyWayOracle.QuasarDataTypeToDataType[quasar_data_type]
        except KeyError:
            return opcua.ua.NodeId(24) # this is temporary


class QuasarClass():
    """Represents a QuasarClass"""
    def __init__(self, objectified_class, milkyway_server):
        # TODO: need objectified class ?
        # should we have a ref to milkyway server
        self.design_inspector = milkyway_server.design_inspector
        self.milkyway_server = milkyway_server
        self._objectified_class = objectified_class
        self.name = objectified_class.attrib['name']

    def _instantiate_type(self, ua_server: opcua.Server, ns_index):
        types_node = ua_server.get_node(opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectTypesFolder))
        types_node.add_object_type(ns_index, self.name) # TODO: wrong address!

    def instantiate_object(self, ua_server: opcua.Server, parent_nodeid: opcua.ua.uatypes.NodeId, name, ns_index):
        if isinstance(parent_nodeid, str):
            parent_nodeid = opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectsFolder)
        logging.error(f'Instantiating quasar class {self.name}: begin')
        #pdb.set_trace()
        requested_node_id = opcua.ua.StringNodeId(name, 2)
        object_nodeid = ua_server.get_node(parent_nodeid).add_object (requested_node_id, name)
        initial_value = "Acs"
        object_node = ua_server.get_node(object_nodeid)
        self._instantiate_methods(ua_server, object_node)
        quasar_object = QuasarObject(self)
        quasar_object._instantiate_cache_variables(ua_server, object_node)
        logging.error(f'Instantiating quasar class: end')
        return quasar_object

    def _instantiate_methods(self, ua_server: opcua.Server, object_node):
        try:
            for method in self._objectified_class.method:
                print(f"Method: {method.attrib['name']}")
                object_node.add_method(1, method.attrib['name'], None)
        except AttributeError:
            pass # it's fine, there are no methods.

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
        # pdb.set_trace()
        # per_design_datatype = self.quasar_class.design_inspector.objecty_cache_variableattrib['datatype']
        self.cache_variables[cv_name].set_value(value)



    def _instantiate_cache_variables(self, ua_server: opcua.Server, object_node):
        try:
            for cv in self.quasar_class._objectified_class.cachevariable:
                print(cv.attrib['name'])
                initial_value = None
                #pdb.set_trace()
                data_type = MilkyWayOracle.quasar_data_type_to_node_id(cv.attrib['dataType'])
                requested_node_id = opcua.ua.StringNodeId(object_node.nodeid.Identifier+'.'+cv.attrib['name'], 2)
                var_node_id = object_node.add_variable(requested_node_id, cv.attrib['name'], initial_value, datatype=data_type)
                var_node = ua_server.get_node(var_node_id)
                self.cache_variables[cv.attrib['name']] = var_node
                setter_name = f"set{cv.attrib['name'].title()}"
                self.cache_variables_setters[setter_name] = cv.attrib['name']
        except AttributeError:
            pass # no cache variables in this class.

    def __getattr__(self, name):
        print(f'getattr on {name}')
        # in case:
        if name in self.cache_variables_setters:
            return lambda *args: self.set_cv(self.cache_variables_setters[name], args[0])
        return super(QuasarObject, self).__getattribute__(name)

    def __call__(self, *args):
        print(f'name= args={args}')

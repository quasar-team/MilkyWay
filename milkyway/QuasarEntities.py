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
        'OpcUa_Double'  : opcua.ua.NodeId(11),
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

    def quasar_data_type_to_variant_type(quasar_data_type):
        '''Will find the stack's variant type from quasars data type, as per Design.
        Example: for "OpcUa_Int16" it shall return opcua.ua.uatypes.VariantType.Int16'''
        if quasar_data_type.startswith('OpcUa_'):
            raw_data_type = quasar_data_type.replace('OpcUa_', '')
            matching_raw_types = [ x for x in opcua.ua.uatypes.VariantType if x.name == raw_data_type]
            if len(matching_raw_types) == 1:
                return matching_raw_types[0]
            else:
                raise Exception(f'datatype {quasar_data_type} unknown or not implemented yet')
        else:
            remaining_types = {
                'UaString' : opcua.ua.uatypes.VariantType.String,
                'UaVariant' : opcua.ua.uatypes.VariantType.Variant
            }
            try:
                return remaining_types[quasar_data_type]
            except KeyError:
                raise NotImplementedError(f'datatype: {quasar_data_type}')

    def quasar_data_type_to_type_def_id(quasar_data_type):
        variant_type = MilkyWayOracle.quasar_data_type_to_variant_type(quasar_data_type)
        # Let's profit from the fact that variant types match type node ids in NS0 for the basic built-in types
        return opcua.ua.NodeId(variant_type.value)


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
        logging.debug(f'Instantiating quasar class {self.name} under parent nodeid {parent_nodeid}: begin')
        #pdb.set_trace()
        if parent_nodeid == opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectsFolder):
            string_addr = name
        else:
            string_addr = parent_nodeid.Identifier + '.' + name
        requested_node_id = opcua.ua.StringNodeId(string_addr, 2)
        logging.debug(f'Requesting node-id: {requested_node_id}')
        object_nodeid = ua_server.get_node(parent_nodeid).add_object (requested_node_id, name)
        initial_value = "Acs"
        object_node = ua_server.get_node(object_nodeid)
        self._instantiate_methods(ua_server, object_node)
        quasar_object = QuasarObject(self)
        quasar_object._instantiate_cache_variables(ua_server, object_node)
        quasar_object.nodeid = object_nodeid.nodeid
        logging.debug(f'Instantiating quasar class: end')
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
                data_type = MilkyWayOracle.quasar_data_type_to_type_def_id(cv.attrib['dataType'])
                requested_node_id = opcua.ua.StringNodeId(object_node.nodeid.Identifier+'.'+cv.attrib['name'], 2)
                var_node_id = object_node.add_variable(requested_node_id, cv.attrib['name'], initial_value, datatype=data_type)
                var_node = ua_server.get_node(var_node_id)
                # if 'array' in cv.attrib['name']:
                #     pdb.set_trace()
                array_elems = [x for x in cv.iter() if x.tag == '{http://cern.ch/quasar/Design}array']
                if len(array_elems) > 0:
                    var_node.set_value_rank(1) # array:
                else:
                    var_node.set_value_rank(0) # scalar

                if cv.get('addressSpaceWrite') in ['regular', 'delegated']:
                    var_node.set_writable(True)
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

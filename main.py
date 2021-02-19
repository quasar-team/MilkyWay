import logging
import opcua
from milkyway import Server
from milkyway.QuasarEntities import QuasarClass

logging.basicConfig(level=logging.ERROR)

server = Server('Design.xml')
SCA = server._quasar_classes['SCA']
objects_nodeid = opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectsFolder)
SCA.instantiate_object(server.ua_server, objects_nodeid, 'sca1', server.quasar_nsi)


server.run()

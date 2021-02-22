import logging
import opcua
from milkyway import Server
from milkyway.QuasarEntities import QuasarClass
import time
import pdb

logging.basicConfig(level=logging.ERROR)

server = Server('Design.xml')
SCA = server._quasar_classes['SCA']
objects_nodeid = opcua.ua.NodeId(opcua.ua.ObjectIds.ObjectsFolder)
sca1_object = SCA.instantiate_object(server.ua_server, objects_nodeid, 'sca1', server.quasar_nsi)
online = sca1_object.cache_variables['online']


server.start()
ctr = 0
while True:
    time.sleep(1)
    ctr += 1
    # sca1_object.set_cv('online', ctr)
    sca1_object.setOnline(ctr)

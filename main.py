import logging
import opcua
from milkyway import Server
from milkyway.QuasarEntities import QuasarClass
import time
import pdb
import quasar_basic_utils

logging.basicConfig(level=logging.ERROR)

try:
    server = Server('Design.xml')
    SCA = server._quasar_classes['SCA']
    sca1_object = SCA.instantiate_object(server.ua_server, '.', 'sca1', server.quasar_nsi)

    server.start()
    ctr = 0
    while True:
        time.sleep(1)
        ctr += 1
        # sca1_object.set_cv('online', ctr)
        sca1_object.setOnline(ctr)
except:
    quasar_basic_utils.quasaric_exception_handler()

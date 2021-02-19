import logging
from milkyway import Server
from milkyway.QuasarEntities import QuasarClass

logging.basicConfig(level=logging.ERROR)

server = Server('Design.xml')
SCA = server._quasar_classes['SCA']
SCA.instantiate_object('.', 'sca1')


server.run()

import logging
from milkyway import Server

logging.basicConfig(level=logging.ERROR)

server = Server('Design.xml')
server.create_object('SCA', 'sca1')
server.run()

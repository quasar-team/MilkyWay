import logging
import argparse
import opcua
from milkyway import Server
from milkyway.QuasarEntities import QuasarClass
import time
import pdb

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--design')
    parser.add_argument('--config')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("opcua").setLevel(logging.ERROR)

    server = Server(args.design)
    server.instantiate_from_config(args.config)
    server.start()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()

import logging
import argparse
import opcua
from milkyway import Server
from milkyway.QuasarEntities import QuasarClass
import quasar_basic_utils
import time
import pdb
import sys

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--design', required=True)
    parser.add_argument('--config')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("opcua").setLevel(logging.ERROR)

    try:
        server = Server(args.design)
        if args.config:
            server.instantiate_from_config(args.config)
        server.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('\nStopping...')
        server.stop()

    except:
        quasar_basic_utils.quasaric_exception_handler()
        sys.exit(1)


if __name__ == '__main__':
    main()

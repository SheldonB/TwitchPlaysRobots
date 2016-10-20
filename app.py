import re
import json
import logging
import argparse

from lib import irc, util

commands = (
        'FORWARD',
        'BACKWARD',
        'TURN'
        )

class ApplicationServer(object):
    def __init__(self, config):
        self.irc = irc.irc(config)
        self.logger = logging.getLogger()

    def run(self):
        while True:
            msg = util.process_message(self.irc.recieve_message())
            if msg is not None:
                self.logger.debug('Message recieved - %s - %s' % (msg['username'], msg['message']))

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', help='Pass in a config file. That specifices sever, user, pass, and channel')
    arg_parser.add_argument('--debug', action='store_true', help='Turn on debugging to recieve logging info') 
    args = arg_parser.parse_args()

    with open(args.config) as config_file:
        config = json.load(config_file)
    
    logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s')
    logger = logging.getLogger()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    app = ApplicationServer(config)
    app.run()

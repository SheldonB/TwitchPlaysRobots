import re
import json
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

    def run(self):
        while True:
            msg = util.process_message(self.irc.recieve_message())
            if msg is not None:
                print(msg)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', help='Pass in a config file. That specifices sever, user, pass, and channel')
    
    args = arg_parser.parse_args()

    with open(args.config) as config_file:
        config = json.load(config_file)

    app = ApplicationServer(config)
    app.run()

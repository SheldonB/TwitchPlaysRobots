import re
import json
import argparse

from lib import irc

commands = (
        'FORWARD',
        'BACKWARD',
        'TURN'
        )

def process_message(msg):
    parsed_msg = parse_message(msg)
    return parsed_msg

def parse_message(msg):
    return {
            'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', msg)[0],
            # 'message':
    }

class ApplicationServer(object):
    def __init__(self, config):
        self.irc = irc.irc(config)

    def run(self):
        while True:
            msg = process_message(self.irc.recieve_message())
            print(msg)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', help='Pass in a config file. That specifices sever, user, pass, and channel')
    
    args = arg_parser.parse_args()

    with open(args.config) as config_file:
        config = json.load(config_file)

    app = ApplicationServer(config)
    app.run()

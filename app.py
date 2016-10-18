import re
import json
import argparse

from lib import irc

commands = (
        'FORWARD',
        'BACKWARD',
        'TURN'
        )

def check_message(msg):
    if re.match(r':[0-9A-Za-z]*![0-9A-Za-z]*@[0-9A-Za-z]*.tmi.twitch.tv PRIVMSG #[0-9A-Za-z]* :[!*0-9A-Za-z_]*', msg):
        return True

def process_message(msg):
    if check_message(msg):
        parsed_msg = parse_message(msg)
        return parsed_msg

def parse_message(msg):
    return {
            'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', msg)[0],
            'message': re.findall(r'PRIVMSG #[0-9A-Za-z]* :([!*0-9A-Za-z_\- ]*)', msg)[0]
    }

class ApplicationServer(object):
    def __init__(self, config):
        self.irc = irc.irc(config)

    def run(self):
        while True:
            # msg = self.irc.recieve_message()
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

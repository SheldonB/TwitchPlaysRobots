import re, json, argparse, logging

from lib import irc, util

class ApplicationServer(object):
    RED_TEAM = 'RED'
    BLUE_TEAM = 'BLUE'
    
    def __init__(self, config):
        self.irc = irc.irc(config)
        self.logger = logging.getLogger()
        self.team_assignments = {}

    def run(self):
        while True:
            msg = util.process_message(self.irc.recieve_message())

            if msg:
                self.logger.debug('Message recieved from %s: %s' % (msg['username'], msg['message']))

            if msg and 'command' in msg:
                self.logger.info('Command recieved from %s: %s %s' % (msg['username'], msg['command'], msg['argument']))

                if msg['command'] == 'JOIN':
                    self._assign_team(msg['username'], msg['argument'])
                else:
                    # TODO: Package message and put in queue to be sent
                    return

    def _assign_team(self, username, team):
        if team == self.RED_TEAM:
            self.team_assignments[username] = self.RED_TEAM
            self.logger.debug('Assigning {} to red team.'.format(username))
        elif team == self.BLUE_TEAM:
            self.team_assignments[username] = self.BLUE_TEAM
            self.logger.debug('Assigning {} to blue team.'.format(username))


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

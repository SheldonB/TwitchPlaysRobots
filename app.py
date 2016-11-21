import queue
import multiprocessing
import re, json, argparse, logging

from lib import irc, util

RED_TEAM = 'RED'
BLUE_TEAM = 'BLUE'

command_queue = multiprocessing.Queue()

class ApplicationLayer(object):

    def __init__(self, config):
        self.irc = irc.irc(config)
        self.logger = logging.getLogger()
        self.team_assignments = {}

    def run(self):
        while True:
            msg = util.process_message(self.irc.recieve_message())

            if msg:
                self.logger.debug('Message recieved from {}: {}'.format(msg['username'],
                    msg['message']))

            if msg and 'command' in msg:
                self.logger.info('Command recieved from {}: {} {}'.format(msg['username'],
                    msg['command'], msg['argument']))

                if msg['command'] == 'JOIN':
                    self._assign_team(msg['username'], msg['argument'])
                else:
                    if msg['username'] in self.team_assignments:
                        msg['team'] = self.team_assignments[msg['username']]
                        self._queue_command(msg)

    def _assign_team(self, username, team):
        if team == RED_TEAM:
            self.team_assignments[username] = RED_TEAM
            self.logger.debug('Assigning {} to red team.'.format(username))
        elif team == BLUE_TEAM:
            self.team_assignments[username] = BLUE_TEAM
            self.logger.debug('Assigning {} to blue team.'.format(username))

    def _queue_command(self, msg):
        command_queue.put(msg)


class ServiceLayer(object):
    def __init__(self):
        self.logger = logging.getLogger()

    def run(self):
        while True:
            try:
                item = command_queue.get()
                print('{} {} {}'.format(item['team'], item['command'], item['argument']))
                if item['team'] == RED_TEAM:
                    print('Send to red')
                elif item['team'] == BLUE_TEAM:
                    print('Send to blue')
            except queue.Empty:
                pass


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

    app = ApplicationLayer(config)
    application_process = multiprocessing.Process(target=app.run)
    application_process.start()

    service = ServiceLayer()
    service_process = multiprocessing.Process(target=service.run)
    service_process.start()


import queue
import multiprocessing
import re, json, argparse, logging, time

from lib import irc, util, rf_24

RED_TEAM = 'RED'
BLUE_TEAM = 'BLUE'

red_command_queue = multiprocessing.Queue()
blue_command_queue = multiprocessing.Queue()

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
        if msg['team'] == RED_TEAM:
            red_command_queue.put(msg)
        elif msg['team'] == BLUE_TEAM:
            blue_command_queue.put(msg)
             

RED_COMPLETE = 'RED_COMPLETE'
BLUE_COMPLETE = 'BLUE_COMPLETE'
TIMEOUT = 5
RED_PIPE = [0xE8, 0xE8, 0xF0, 0xF0, 0xE1]
BLUE_PIPE = [0xE8, 0xE8, 0xF0, 0xF0, 0xE2]

class ServiceLayer(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.radio = rf_24.Radio()
        self.RED_STATUS = True
        self.BLUE_STATUS = True

    def run(self):
        last_red_msg_sent = 0
        last_blue_msg_sent = 0
        while True:
            msg = self.radio.recieve_message()

            if msg and msg == RED_COMPLETE:
                self.logger.debug('Recieved complete from red')
                self.RED_STATUS = True
                time.sleep(1)
            elif msg and msg == BLUE_COMPLETE:
                self.logger.debug('Recieved complete from blue')
                self.BLUE_STATUS = True
                time.sleep(1)
            
            if time.time() - last_red_msg_sent > TIMEOUT and not self.RED_STATUS:
                self.logger.debug('Timeout reached after sending packet to red')
                self.RED_STATUS = True

            if time.time() - last_blue_msg_sent > TIMEOUT and not self.BLUE_STATUS:
                self.logger.debug('Timeout reached after sending packet to blue')
                self.BLUE_STATUS = True

            if  self.RED_STATUS:
                try:
                    item = red_command_queue.get_nowait()
                    self.logger.debug('Sending packet: TEAM:{} COMMAND:{} ARGUMENT:{}'.format(
                                      item['team'], item['command'], item['argument']))
                    self.radio.send_message('{}:{}'.format(item['command'], item['argument']), RED_PIPE)
                    self.RED_STATUS = False
                    last_red_msg_sent = time.time()
                except queue.Empty:
                    pass

            if self.BLUE_STATUS:
                try:
                    item = blue_command_queue.get_nowait()
                    self.logger.debug('Sending packet: TEAM:{} COMMAND:{} ARGUMENT:{}'.format(
                                      item['team'], item['command'], item['argument']))
                    self.radio.send_message('{}:{}'.format(item['command'], item['argument']), BLUE_PIPE)
                    self.BLUE_STATUS = False
                    last_blue_msg_sent = time.time()
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


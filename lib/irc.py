import socket, sys, logging

class irc(object):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger()
        self.sock = self.get_socket_connection()

    def _check_ping(self, data):
        if data[:4] == 'PING':
            return True

    def recieve_message(self):
        data = self.sock.recv(1024).decode('utf-8')
        if self._check_ping(data):
            self.logger.debug('Sending Pong')
            self.sock.send(b'PONG')
            return None
        return data
   
    def send_message(self, message):
        self.sock.send(bytes('PRIVMSG %s :%s\r\n' % (self.config['channel'], message), 'utf-8'))
        self.logger.send('Sending Message: %s' % (message))

    def get_socket_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        try:
            sock.connect((self.config['server'], self.config['port']))
        except:
            self.logger.exception('Unable to connect to %s:%s' % (self.config['server'], self.config['port']))
            sys.exit()

        sock.settimeout(None)

        sock.send(bytes('USER %s\r\n' % (self.config['username']), 'utf-8'))
        sock.send(bytes('PASS %s\r\n' % (self.config['password']), 'utf-8'))
        sock.send(bytes('NICK %s\r\n' % (self.config['username']), 'utf-8'))


        sock.send(bytes('JOIN %s\r\n' % (self.config['channel']), 'utf-8'))

        self.logger.info('Successful connection to %s:%s' % (self.config['server'], self.config['port']))
        return sock


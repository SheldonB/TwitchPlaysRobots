import socket, sys

class irc(object):
    def __init__(self, config):
        self.config = config
        self.sock = self.get_socket_connection()

    def _check_ping(self, data):
        if data[:4] == 'PING':
            return True

    def recieve_message(self):
        data = self.sock.recv(1024).decode('utf-8')
        if self._check_ping(data):
            print('Sending Pong')
            self.sock.send('PONG')
        return data
   
    def send_message(self, message):
        self.sock.send(bytes('PRIVMSG %s :%s\r\n' % (self.config['channel'], message), 'utf-8'))

    def get_socket_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        try:
            sock.connect((self.config['server'], self.config['port']))
        except:
            print('Unable to connect to %s:%s' % (self.config['server'], self.config['port']))
            sys.exit()

        sock.settimeout(None)

        sock.send(bytes('USER %s\r\n' % (self.config['username']), 'utf-8'))
        sock.send(bytes('PASS %s\r\n' % (self.config['password']), 'utf-8'))
        sock.send(bytes('NICK %s\r\n' % (self.config['username']), 'utf-8'))


        sock.send(bytes('JOIN %s\r\n' % (self.config['channel']), 'utf-8'))

        return sock

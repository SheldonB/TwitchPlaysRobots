import re, logging

logger = logging.getLogger()

COMMAND_TABLE = (
            'FORWARD',
            'BACKWARD',
            'TURN',
            'JOIN'
        )

def process_message(msg):
    if _check_message(msg):
        parsed_msg = _parse_message(msg)
        return parsed_msg

def _check_message(msg):
    if re.match(r':[0-9A-Za-z]*![0-9A-Za-z]*@[0-9A-Za-z]*.tmi.twitch.tv PRIVMSG #[0-9A-Za-z]* :[!*0-9A-Za-z_]*', msg):
        return True

def _parse_message(msg):
    parsed_msg = re.findall(r'PRIVMSG #[0-9A-Za-z]* :([!*0-9A-Za-z_\- ]*)', msg)[0]

    if _check_command(parsed_msg):
        command = _parse_command(parsed_msg)
        argument = _parse_argument(parsed_msg)

        return {
                'username': re.findall(r'^:([A-Za-z0-9_]+)\!', msg)[0],
                'message': parsed_msg,
                'command': command,
                'argument': argument
        }

    return {
            'username': re.findall(r'^:([A-Za-z0-9_]+)\!', msg)[0],
            'message': parsed_msg,
    }

def _check_command(msg):
    if re.match(r'![a-zA-Z]* ?[A-Za-z0-9]*', msg):
        parsed_command = _parse_command(msg)
        for command in COMMAND_TABLE:
            if parsed_command == command:
                return True
    return False

def _parse_command(msg):
    return re.findall(r'!([A-Za-z]*)', msg)[0].upper()

def _parse_argument(command):
    """ Parse out the argument from the
    command. This argument is for the amount
    to move forward of backwards and then the
    degrees to turn. If no argument is found
    then the argument is set to 1.
    """
    argument = re.findall(r'![A-Za-z]* ([A-Za-z0-9]*)', command)
    if not argument:
        argument = 1
    else:
        argument = argument[0].upper()
    return argument

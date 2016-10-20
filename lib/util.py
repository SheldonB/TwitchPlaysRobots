import re

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
        argument = _parse_argument(command)

        return {
                'username': re.findall(r'^:([a-za-z0-9_]+)\!', msg)[0],
                'message': parsed_msg,
                'command': command,
                'arguement': argument
        }

    return {
            'username': re.findall(r'^:([a-za-z0-9_]+)\!', msg)[0],
            'message': parsed_msg,
    }

def _check_command(msg):
    if re.match(r'![a-zA-Z]* ?[0-9]*', msg):
        return True

def _parse_command(msg):
    return re.findall(r'!([A-Za-z]*)', msg)[0]

def _parse_argument(command):
    argument = re.findall(r'[A-Za-z]* ([0-9]*)', command)
    if not argument:
        argument = 1
    else:
        argument = argument[0]
    return argument

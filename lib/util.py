import re

def process_message(msg):
    if _check_message(msg):
        parsed_msg = _parse_message(msg)
        return parsed_msg

def _check_message(msg):
    if re.match(r':[0-9A-Za-z]*![0-9A-Za-z]*@[0-9A-Za-z]*.tmi.twitch.tv PRIVMSG #[0-9A-Za-z]* :[!*0-9A-Za-z_]*', msg):
        return True

def _parse_message(msg):
    return {
            'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', msg)[0],
            'message': re.findall(r'PRIVMSG #[0-9A-Za-z]* :([!*0-9A-Za-z_\- ]*)', msg)[0]
    }

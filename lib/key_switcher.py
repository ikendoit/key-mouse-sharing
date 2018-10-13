# pynput of the host does not auto accept special keys as string 
# this module convert the Object into the right String to send to server
# Author: Ken Nguyen
from . import keys_map 
keys_map_dict = keys_map.keys_map
keys_command = keys_map.keys_command

def switch_key(key_code):
    return keys_map_dict.get(key_code, None)

def key_need_up(key_string): 
    for item in keys_command:
        action, keyStr = item.split('-')[0:2]
        if keyStr == key_string:    
            return action

    return 'down'

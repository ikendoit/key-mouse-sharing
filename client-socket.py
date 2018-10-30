#!/usr/bin/env python3
# Client script to receive key strokes and mouse actions from host and execute on client machine
# Author: Ken Nguyen

'''
Simple client that receives
  - Key board event. (priority since I use vim for chrome mainly 
  - mouse event. (second-priority since I don't use alot of mouse) 
  - Hopefully: have a error handling mechanism that will auto close when in infinite loop
'''

import socket 
import re
import sys
import pyautogui
from pynput.mouse import Controller, Button

# Improve performance, pyautogui has a 'fail-safe', where you get 0.1s to move the mouse to 0,0 to exit. https://stackoverflow.com/questions/46736652/pyautogui-press-causing-lag-when-called
# Let's remove that for now. May find other ways in the future
pyautogui.PAUSE=0
# same thing for: https://github.com/asweigart/pyautogui/issues/67, which seems to end up with a Java praise ?!
pyautogui.MINIMUM_DURATION=0
pyautogui.MINIMUM_SLEEP=0
holding_key = None
numberBuffer = 0 
mouse = Controller()

# TODO: test shift-... or alt-tab 

def perform_according(cmd):
    global holding_key
    global numberBuffer
    try :
        # keyboard performer -- used by client
        #splitted_cmd = cmd.split('-')
        #if len(splitted_cmd) < 2: #    print('bad reply, connection ended. {0}'.format(cmd))
        #    sys.exit(1)
        #action, key = splitted_cmd[0:2]
        #action = action[2:]
        #key = key[:-2]
        #print(action, key)
        action_key = None
        try :
            action_key = re.match(r'<<(.*)>>',cmd)[1].split('>><<')[0]
            action, key = action_key.split('-')
        except: 
            pass
        print(action, key)
        if action == 'press':    
            if holding_key:
                print('PERFORMING HOLDING KEY: ',holding_key)
                pyautogui.keyDown(holding_key)
                pyautogui.press(key)
                pyautogui.keyUp(holding_key)
            else :
                pyautogui.press(key)
        if action == 'down':    
            print('HOLDING KEY IS:', holding_key)
            pyautogui.keyDown(key)
            holding_key=key
        elif action == 'up':    
            pyautogui.keyUp(holding_key)
            pyautogui.keyUp(key)
            holding_key=None
        elif action == 'move': 
            action = {
                'left': [-10,0],
                'down': [0,10],
                'up': [0,-10],
                'right': [10,0],
            }.get(key)
            if type(action) == 'list': 
                try :
                    num=int(key.char)
                    numberBuffer= numberBuffer*10
                    numberBuffer= numberBuffer+num
                except Exception as err:
                    pass
            elif action == 'l-click':
                try :
                    pyautogui.click()
                except Exception as err:
                    pass
            elif action == 'r-click':
                try :
                    pyautogui.click(button='right')
                except Exception as err:
                    pass
    except Exception as err:
        print(err)
        return False

def parseLastRequest(req) :
    print(req)


def chatConnection(host): 
    print('waiting for host...\n')
    HOST = host
    PORT = 31998
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.connect((HOST, PORT))
    loading=False

    while True: 
        reply = s.recv(4096).decode()
        if loading: continue
        loading=True
        perform_according(reply)
        loading=False
    s.close()

chatConnection(sys.argv[1] if len(sys.argv) > 1 else 'localhost')

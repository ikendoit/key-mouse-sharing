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
        action_key = None
        action = None,
        key = None
        try :
            action_key = re.match(r'<<(.*)>>',cmd)[1].split('>><<')[0]
            action, key = action_key.split('-')
        except:
            pass
        print(action, key, action_key)
        if not action and not key:
            return False
        if action == 'press':
            if holding_key:
                print('PERFORMING HOLDING KEY: ',holding_key)
                pyautogui.keyDown(holding_key)
                pyautogui.press(key)
                pyautogui.keyUp(holding_key)
            else :
                pyautogui.press(key)

            # capture number presses to add to numberBuffer
            try :
                num=int(key)
                numberBuffer= numberBuffer*10+num
                print('new numberBuffer: ',numberBuffer)
            except Exception as err:
                print(err)
                numberBuffer = 0
                pass
        if action == 'down':
            pyautogui.keyDown(key)
            holding_key=key
        elif action == 'up':
            pyautogui.keyUp(key)
            # NOTE: cannot do: ctrl+shift+w, since we only record 1 holding key atm.
            holding_key=None
        elif action == 'move':
            mouse_action = {
                'left': [-10,0],
                'down': [0,10],
                'up': [0,-10],
                'right': [10,0],
                'lclick': 'lclick',
                'rclick': 'rclick',
            }.get(key)
            if type(mouse_action) == type([]):
                try :
                    current_position = pyautogui.position()
                    newX = current_position[0] + mouse_action[0]*(numberBuffer+1)
                    newY = current_position[1] + mouse_action[1]*(numberBuffer+1)
                    numberBuffer = 0
                    print('moving to: ',newX, newY)
                    pyautogui.moveTo(newX, newY)
                except Exception as err:
                    print('move err: ',err)
                    pass
            elif mouse_action == 'lclick':
                try :
                    print('left clicking')
                    pyautogui.click()
                except Exception as err:
                    print('click left err: ',err)
                    pass
            elif mouse_action == 'rclick':
                try :
                    print('right clicking')
                    pyautogui.click(button='right')
                except Exception as err:
                    print('click right err: ',err)
                    pass
    except Exception as err:
        print(err)
        return False

def parseLastRequest(req) :
    print(req)


def startConnection(host): 
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
        result = perform_according(reply)
        if result == False: 
            print('ending Connection')
            return None
        loading=False
    s.close()

startConnection(sys.argv[1] if len(sys.argv) > 1 else 'localhost')

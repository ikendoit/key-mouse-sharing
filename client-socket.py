#!/usr/bin/env python3

'''
Simple client that receives
  - Key board event. (priority since I use vim for chrome mainly 
  - mouse event. (second-priority since I don't use alot of mouse) 
  - Hopefully: have a error handling mechanism that will auto close when in infinite loop
'''

import socket 
import sys
import pyautogui

def perform_according(cmd):
    # keyboard performer -- used by client
    action, key = cmd.split('-')
    if action == 'down':    
        pyautogui.keyDown(key)
    elif action == 'up':    
        pyautogui.keyUp(key)
    elif action == 'move': 
        x,y = key.split(',')
        # should use moveRel(dx,dy)
        pyautogui.moveTo(x,y)
    elif action == 'click':
        x,y,button,mouse_action = key.split(',')
        # should use moveRel
        # should consider dragging
        # should consifer holding/releasing (for mouse_action)
        pyautogui.moveTo(x,y)
        pyautogui.click(button)


def chatConnection(host): 
    print('waiting for host...\n')
    HOST = host or 'localhost'
    PORT = 31998
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.connect((HOST, PORT))

    while True: 
        reply = s.recv(4096).decode()
        perform_according(reply)
        print('\n[HOST]> {0}'.format(reply))
    s.close()

chatConnection(sys.argv[0])

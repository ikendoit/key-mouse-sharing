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
    cmd.split('-')
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    
    pyautogui.press('9')
    pyautogui.press('j')
    pyautogui.press('j')
    pyautogui.press('j')
    pyautogui.press('j')
    pyautogui.press('f')



def chatConnection(): 
    print('waiting for host...\n')
    HOST = 'localhost'
    PORT = 31998
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.connect((HOST, PORT))

    while True: 
        reply = s.recv(4096).decode()
        perform_according(reply)
        print('\n[HOST]> {0}'.format(reply))
    s.close()

chatConnection()

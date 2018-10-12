#!/usr/bin/env python3

'''
The server that will
  - record and capture keyboard of host machine and send to client to executes 
  - same for mouse events: move + click
  - Hopefully: Interrupt keyboard + mouse events of host machine, so that we can actually focus on the client machine
'''

import socket
import sys
from pynput import keyboard, mouse
from lib import special_key_switcher
from lib import special_mouse_switcher
HOST = '0.0.0.0'
PORT = 31998

def start_server():
    # socket connection for inter-computer connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    connection, addr = s.accept()

    while True: 
        # keyboard listener -- used by host
        def on_press(key):
            try:
                connection.send('press-{0}'.format(key.char).encode())
            except AttributeError:
                keyStr = special_key_switcher.switch_key(key)
                connection.send(keyStr.encode())
                print('special key {0} pressed'.format(key))

        def on_release(key):
            connection.send('up-{0}'.format(str(key)).encode())
            if key == keyboard.Key.f1:    
                return False

        def on_move(x,y):
            connection.send('move-{0},{1}'.format(str(x), str(y)).encode())

        def on_click(x,y,button, pressed):  
            connection.send('click-{0},{1},{2},{3}'
                .format(
                    str(x), 
                    str(y), 
                    special_mouse_switcher.switch_button(button),
                    'Pressed' if pressed else 'Released'
                ).encode())
        def on_scroll(x, y, dx, dy):
            connection.send('scroll-{0},{1},{2},{3}'
                .format(
                    str(x), 
                    str(y),
                    str(dx),
                    str(dy),
                ).encode())

        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as kb_listener: 

            with mouse.Listener(
                    on_move=on_move,
                    on_click=on_click,
                    on_scroll=on_scroll) as m_listener: 

                m_listener.join()
                kb_listener.join()

    connection.close()

start_server()

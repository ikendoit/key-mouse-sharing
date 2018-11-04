#!/usr/bin/env python3
# host machine scripts to send host's keys and mouse to client
# Author: Ken Nguyen

'''
The server that will
  - record and capture keyboard of host machine and send to client to executes 
  - same for mouse events: move + click
  - Hopefully: Interrupt keyboard + mouse events of host machine, so that we can actually focus on the client machine
'''

import socket
import sys
import threading 

from classes import Host
HOST = '0.0.0.0'
PORT = 31998

def accept_client(connection,addr):
    my_client = Host.HostScript(connection)
    my_client.runController()


def start_server():
    # socket connection for inter-computer connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    while True: 
        connection, addr = s.accept()
        print('initiated with client')
        #threading.Thread(target = accept_client,args = (connection,addr)).start()
        accept_client(connection,addr)
    print('closing all connection')
    connection.close()

start_server()

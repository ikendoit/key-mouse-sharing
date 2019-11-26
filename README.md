# Key Mouse Sharing 

This read me is written in another keyboard ( using Thinkpad's key board, remotely control Asus keyboard to type this read me )

First, let's procrastinate: https://www.youtube.com/watch?v=zpN7Ait0sOE&t=52s

## Author's Note: 
```
There seem to be a bug, where python3-xlib threading is conflicting with linux Xorg display server. 
I will continue to research on this bug. while so, this project will be delayed. 
This bug exists in this question, which no one has answered yet. https://stackoverflow.com/questions/52935700/how-do-i-properly-terminate-pynput-calls-now-it-makes-my-x-crash-self-socket
```

## Installation (On Linux)

Download [Python3](https://www.python.org/downloads/)

```
  ## installing pyautogui
  sudo apt-get install scrot python3-tk python3-dev 
  pip3 install pyautogui python3-xlib pynput
```

or follow this page: https://pyautogui.readthedocs.io/en/latest/install.html

## How to run: 

```
  <host machine:>
    ifconfig | grep inet
    <get ip address>
    python3 index.py

  <client machine:>
    python3 client-socket.py <ip of host>

  <start typing on host machine>
```

## How to use

```
./mouse_controller.py
<click f2 to control mouse, esc to exit mouse mode>
<click f1 to control client, esc to exit client mode >
< up down left right to move mouse >
< right_ctrl, right_shift to left/right click >

```

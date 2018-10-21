# Key Mouse Sharing 

This read me is written in another keyboard

## Installation (Linux)
```
  sudo apt-get install scrot python3-tk python3-dev

  pip3 install pyautogui python3-xlib pynput
```

or follow this page: https://pyautogui.readthedocs.io/en/latest/install.html

## RUN: 

```
  <host machine:>
    ifconfig | grep inet
    <get ip address>
    python3 index.py

  <client machine:>
    python3 client-socket.py <ip of host>

  <start typing on host machine>
```

# MOUSE CONTROLLER

##RUN

```
	./mouse_controller.py
	<click f3 to control mouse, f1 to exit mouse mode but can return>
	< 'hjkl' to move around >
	< 'io' to left/right click >

```

#!/usr/bin/env python3
# Author: Ken Nguyen

from pynput import keyboard, mouse
import pyautogui

# host machine, you can move mouse using key board
# but using vim syntax
def keyboard_does_mouse():
    def on_press_kdm(key):
        try : 
            action = {
                'h': [-10,0],
                'j': [0,10],
                'k': [0,-10],
                'l': [10,0],
                'H': [-30,0],
                'J': [0,30],
                'K': [0,-30],
                'L': [30,0],
                'i': 'left',
                'o': 'right'
            }.get(key.char)
            if not action: return
            if type(action) is str:
                pyautogui.click(button=action)
            elif type(action) is list:
                pos = pyautogui.position()
                newPos = []
                newPos.append(pos[0]+action[0])
                newPos.append(pos[1]+action[1])
                pyautogui.moveTo(newPos) 
        except AttributeError:
            print('special key')

    def on_release_kdm(key):
        if key == keyboard.Key.f1:    
            return False

    with keyboard.Listener(
        on_press=on_press_kdm,
        on_release=on_release_kdm,
        suppress=True) as kb_listener_child: 
            kb_listener_child.join()


def runController(): 

    def on_release(key):
        if key == keyboard.Key.f3:    
            keyboard_does_mouse()

    with keyboard.Listener(
        on_release=on_release,
        suppress=False) as kb_listener_controller: 
            kb_listener_controller.join()

runController()


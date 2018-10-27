#!/usr/bin/env python3
# Author: Ken Nguyen

from pynput import keyboard, mouse
import pyautogui
mouse_ctl = mouse.Controller()
numberBuffer = 0 

# host machine, you can move mouse using key board
# but using vim syntax
def keyboard_does_mouse():
    def on_press_kdm(key):
        global numberBuffer
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
            # action is caught successfully
            if not action: 
                try :
                    num=int(key.char)
                    numberBuffer= numberBuffer*10
                    numberBuffer= numberBuffer+num
                except Exception as err:
                    print(err)
                    pass
                return
            if type(action) is str:
                pyautogui.click(button=action)
            elif type(action) is list:
                #pos = pyautogui.position()
                #newPos = []
                #newPos.append(pos[0]+action[0])
                #newPos.append(pos[1]+action[1])
                #if numberBuffer > 0: 
                #    print('performing number: ',numberBuffer)
                #    newPos[0] = newPos[0]+action[0]*numberBuffer
                #    newPos[1] = newPos[1]+action[1]*numberBuffer
                #pyautogui.moveTo(newPos) 
                #numberBuffer = 0

                dx = action[0] + action[0]*numberBuffer
                dy = action[1] + action[1]*numberBuffer
                numberBuffer = 0
                mouse_ctl.move(dx,dy)
        except AttributeError:
            print('special key')

    def on_release_kdm(key):
        if key == keyboard.Key.enter:    
            return False

    with keyboard.Listener(
        on_press=on_press_kdm,
        on_release=on_release_kdm,
        suppress=True) as kb_listener_child: 
            kb_listener_child.join()


def runController(): 

    def on_release(key):
        if key == keyboard.Key.f1:    
            keyboard_does_mouse()

    with keyboard.Listener(
        on_release=on_release,
        suppress=False) as kb_listener_controller: 
            kb_listener_controller.join()
    print('at line 79')

runController()


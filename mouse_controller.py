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
       global numberbuffer
            try : 
                action = {
                    'left': [-10,0],
                    'down': [0,10],
                    'up': [0,-10],
                    'right': [10,0],
                    'lclick': 'lclick',
                    'rclick': 'rclick',
                }.get(key.char)
                # action is caught successfully
                if type(action) == type([]):
                    try :
                        current_position = pyautogui.position()
                        newx = current_position[0] + action[0]*(numberbuffer+1)
                        newy = current_position[1] + action[1]*(numberbuffer+1)
                        numberbuffer = 0
                        print('moving to: ',newx, newy)
                        pyautogui.moveto(newx, newy)
                    except exception as err:
                        print('move err: ',err)
                        pass
                elif action == 'lclick':
                    try :
                        print('left clicking')
                        pyautogui.click()
                    except exception as err:
                        print('click left err: ',err)
                        pass
                elif action == 'rclick':
                    try :
                        print('right clicking')
                        pyautogui.click(button='right')
                    except exception as err:
                        print('click right err: ',err)
                        pass
            except exception as err:
                print(err)
                return false



    def on_release_kdm(key):
        if key == keyboard.Key.esc:    
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


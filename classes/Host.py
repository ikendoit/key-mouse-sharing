from pynput import keyboard, mouse
import pyautogui
from lib import key_switcher
from lib import mouse_switcher

holding_key = None
numberBuffer = 0

class HostScript:
    def __init__(self, connection):
        self.connection = connection

    # child is run when the host machine wants to go to other machine
    # and only send key from host -> client, but block host's subsequent execution
    def runChild(self) :
        def on_press(key):
            try:
                # using <<..>> because:
                # socket seems to throttle packets, 
                # when on_mouse_move works, it generates too many packets and too fast 
                # socket throttles a bit (~0.1s?) and then sends 3-4 packets to the client. So we use <<..>> to identify separate packets.
                self.connection.send('<<press-{0}>>'.format(key.char).encode())
                print('sending to client: press-',key)
            except AttributeError:
                keyStr = key_switcher.switch_key(key)
                print('sending to client: ',keyStr)
                self.connection.send('<<{0}>>'.format(keyStr).encode())

        def on_release(key):
            #if key_switcher.key_need_up(str(key)) == 'down':
                # keys that only 'press' does not need to do .keyUp()
            print('release in client: ', key)
            self.connection.send('<<up-{0}>>'.format(str(key)).encode())
            if key == keyboard.Key.esc:    
                print('exditing client')
                return False

        # removed mouse-listener, as socket connection does not work fast enough for mouse
        # control client mouse with key board for now
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release,
                suppress=True) as kb_listener: 
            print('start joining')
            kb_listener.join()
            print('ended joining')







    def keyboard_does_mouse(self):
        def on_press_kdm(keyObj):
            global numberBuffer
            try:
                key = keyObj.char
            except Exception: 
                key = key_switcher.switch_key(keyObj).split('-')[1]

            try : 
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
                else:
                    # check if number to add to buffer
                    try :
                        num=int(key)
                        numberBuffer= numberBuffer*10+num
                        print('new numberBuffer: ',numberBuffer)
                    except Exception:
                        numberBuffer = 0
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


    def runController(self): 
        def on_release(key):
            if key == keyboard.Key.f1:    
                print('running child connection')
                self.runChild()
                print('finish running child')
            if key == keyboard.Key.f2:    
                print('running key-mouse connection')
                self.keyboard_does_mouse()

        with keyboard.Listener(
            on_release=on_release
            ) as kb_listener_controller: 
                print('start joining controller')
                kb_listener_controller.join()
                print('end joining controller')
        print('finish with, controller')

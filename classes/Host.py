from pynput import keyboard, mouse
from lib import key_switcher
from lib import mouse_switcher
#mouseController = mouse.Controller()

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
                print('sending to client: ',key)
                self.connection.send('<<press-{0}>>'.format(key.char).encode())
            except AttributeError:
                keyStr = key_switcher.switch_key(key)
                self.connection.send(keyStr.encode())

        def on_release(key):
            #if key_switcher.key_need_up(str(key)) == 'down':
                # keys that only 'press' does not need to do .keyUp()
            print('release in client: ', key)
            self.connection.send('<<up-{0}>>'.format(str(key)).encode())
            if key == keyboard.Key.esc:    
                print('exditing client')
                return False

        def on_move(x,y):
            self.connection.send('<<move-{0},{1}>>'.format(str(x), str(y)).encode())

        def on_click(x,y,button, pressed):  
            self.connection.send('<<click-{0},{1},{2},{3}>>'
                .format(
                    str(x), 
                    str(y), 
                    mouse_switcher.switch_button(button),
                    'Pressed' if pressed else 'Released'
                ).encode())
        def on_scroll(x, y, dx, dy):
            self.connection.send('<<scroll-{0},{1},{2},{3}>>'
                .format(
                    str(x), 
                    str(y),
                    str(dx),
                    str(dy),
                ).encode())

        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release,
                suppress=True) as kb_listener: 

            with mouse.Listener(
                    on_move=on_move,
                    on_click=on_click,
                    on_scroll=on_scroll,
                    suppress=True) as m_listener: 

                m_listener.join()
                print('start joining')
                kb_listener.join()
                print('ended joining')


    def runController(self): 
        def on_release(key):
            if key == keyboard.Key.f2:    
                print('running child connection')
                self.runChild()
                print('finish running child')
            if key == keyboard.Key.f3:    
                print('running key-mouse connection')
                #self.keyboard_does_mouse()

        with keyboard.Listener(
            on_release=on_release
            ) as kb_listener_controller: 
                print('start joining controller')
                kb_listener_controller.join()
                print('end joining controller')
        print('finish with, controller')

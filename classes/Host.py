from pynput import keyboard, mouse
from lib import key_switcher
from lib import mouse_switcher

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
            except AttributeError:
                keyStr = key_switcher.switch_key(key)
                self.connection.send(keyStr.encode())
                print('special key {0} pressed'.format(key))

        def on_release(key):
            if key_switcher.key_need_up(str(key)) == 'down':
                # keys that only 'press' does not need to do .keyUp()
                connection.send('<<up-{0}>>'.format(str(key)).encode())
            if key == keyboard.Key.f1:    
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
                on_release=on_release) as kb_listener: 

            with mouse.Listener(
                    on_move=on_move,
                    on_click=on_click,
                    on_scroll=on_scroll) as m_listener: 

                m_listener.join()
                kb_listener.join()

    # host machine, you can move mouse using key board
    # but using vim syntax
    def keyboard_does_mouse(self):
        def on_press_kdm(key):
            a='placeholder' 

        def on_release_kdm(key):
            print('released key does mouse',key)
            if key == keyboard.Key.f1:    
                return False


        with keyboard.Listener(
            on_press=on_press_kdm,
            on_release=on_release_kdm,
            suppress=True) as kb_listener_child: 
                kb_listener_child.join()


    def runController(self): 
        def on_release(key):
            print('released parent',key)
            if key == keyboard.Key.f2:    
                self.runChild()
            if key == keyboard.Key.f3:    
                self.keyboard_does_mouse()

        with keyboard.Listener(
            on_release=on_release,
            suppress=False) as kb_listener_controller: 
                kb_listener_controller.join()


